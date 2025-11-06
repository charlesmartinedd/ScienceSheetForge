"""
Security tests for ScienceSheetForge
Tests input validation, path traversal prevention, and other security features
"""
import os
import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, validate_filename


class SecurityTests(unittest.TestCase):
    """Test security features and input validation"""

    def setUp(self):
        """Set up test client"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_path_traversal_prevention_view(self):
        """Test that path traversal attacks are blocked in view endpoint"""
        malicious_filenames = [
            '../etc/passwd',
            '..\\..\\windows\\system32\\config\\sam',
            'test/../../../etc/passwd',
            '....//....//etc/passwd',
            '%2e%2e%2f%2e%2e%2fetc%2fpasswd',
        ]

        for filename in malicious_filenames:
            response = self.client.get(f'/view/{filename}')
            # Should return 400 (Bad Request) or 403 (Forbidden), not 200
            self.assertIn(response.status_code, [400, 403, 404],
                         f"Path traversal not blocked for: {filename}")

    def test_path_traversal_prevention_download(self):
        """Test that path traversal attacks are blocked in download endpoint"""
        malicious_filenames = [
            '../secret.txt',
            'test/../../app.py',
            './../requirements.txt',
        ]

        for filename in malicious_filenames:
            response = self.client.get(f'/download/{filename}')
            self.assertIn(response.status_code, [400, 403, 404],
                         f"Path traversal not blocked for: {filename}")

    def test_validate_filename_function(self):
        """Test filename validation function"""
        # Valid filenames
        valid_filenames = [
            'worksheet_test.png',
            'crossword_K-LS1-1_20241106.png',
            'test_ANSWER_KEY.png',
        ]

        for filename in valid_filenames:
            self.assertTrue(validate_filename(filename),
                          f"Valid filename rejected: {filename}")

        # Invalid filenames
        invalid_filenames = [
            '../test.png',
            'test/../other.png',
            'test.txt',
            'test.png.exe',
            '../../etc/passwd',
            '',
            None,
            'test/.png',
            'test\\test.png',
        ]

        for filename in invalid_filenames:
            self.assertFalse(validate_filename(filename),
                           f"Invalid filename accepted: {filename}")

    def test_generate_input_validation(self):
        """Test input validation on generate endpoint"""
        # Test missing data
        response = self.client.post('/generate',
                                    json={},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test invalid grade level
        response = self.client.post('/generate',
                                    json={
                                        'grade_level': 'INVALID',
                                        'standard_code': 'K-LS1-1',
                                        'worksheet_format': 'crossword'
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test invalid standard code (SQL injection attempt)
        response = self.client.post('/generate',
                                    json={
                                        'grade_level': 'K-2',
                                        'standard_code': "'; DROP TABLE standards; --",
                                        'worksheet_format': 'crossword'
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test invalid worksheet format
        response = self.client.post('/generate',
                                    json={
                                        'grade_level': 'K-2',
                                        'standard_code': 'K-LS1-1',
                                        'worksheet_format': '../../../etc/passwd'
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_security_headers_present(self):
        """Test that security headers are added to responses"""
        response = self.client.get('/')

        # Check for security headers
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')

        self.assertIn('X-Frame-Options', response.headers)
        self.assertEqual(response.headers['X-Frame-Options'], 'SAMEORIGIN')

        self.assertIn('X-XSS-Protection', response.headers)

        self.assertIn('Content-Security-Policy', response.headers)

    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'ScienceSheetForge')
        self.assertIn('version', data)
        self.assertIn('available_formats', data)

    def test_no_stack_trace_in_error_response(self):
        """Test that error responses don't expose stack traces"""
        # Trigger an error with invalid but validated input
        response = self.client.post('/generate',
                                    json={
                                        'grade_level': 'K-2',
                                        'standard_code': 'NONEXISTENT',
                                        'worksheet_format': 'crossword'
                                    },
                                    content_type='application/json')

        # Error response should not contain implementation details
        data = response.get_json()
        if not data['success']:
            error_msg = data.get('error', '').lower()
            # Should not expose Python internals
            self.assertNotIn('traceback', error_msg)
            self.assertNotIn('exception', error_msg)
            self.assertNotIn('.py', error_msg)


if __name__ == '__main__':
    unittest.main()

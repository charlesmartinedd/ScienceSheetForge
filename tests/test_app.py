"""
Unit tests for Flask application
Tests routes, error handling, and core functionality
"""
import os
import sys
import unittest
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, cleanup_old_files
from ngss_standards import NGSS_STANDARDS


class AppTests(unittest.TestCase):
    """Test Flask application endpoints"""

    def setUp(self):
        """Set up test client"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        # Create temp output folder for tests
        self.test_output = tempfile.mkdtemp(prefix='test_output_')
        self.original_output_folder = self.app.config['OUTPUT_FOLDER']
        self.app.config['OUTPUT_FOLDER'] = self.test_output

    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_output):
            shutil.rmtree(self.test_output, ignore_errors=True)
        self.app.config['OUTPUT_FOLDER'] = self.original_output_folder

    def test_index_page_loads(self):
        """Test that index page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ScienceSheetForge', response.data)

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIsInstance(data['available_formats'], list)

    def test_generate_valid_request(self):
        """Test worksheet generation with valid data"""
        # Get first available standard
        for grade_level, standards in NGSS_STANDARDS.items():
            if standards:
                standard = standards[0]
                break

        response = self.client.post('/generate',
                                    json={
                                        'grade_level': grade_level,
                                        'standard_code': standard['code'],
                                        'worksheet_format': 'crossword'
                                    },
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('worksheet', data)
        self.assertIn('answer_key', data)

    def test_generate_missing_data(self):
        """Test generation with missing required fields"""
        response = self.client.post('/generate',
                                    json={},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_generate_invalid_format(self):
        """Test generation with invalid worksheet format"""
        response = self.client.post('/generate',
                                    json={
                                        'grade_level': 'K-2',
                                        'standard_code': 'K-LS1-1',
                                        'worksheet_format': 'nonexistent_format'
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_view_nonexistent_file(self):
        """Test viewing a file that doesn't exist"""
        response = self.client.get('/view/nonexistent_file.png')
        self.assertEqual(response.status_code, 404)

    def test_download_nonexistent_file(self):
        """Test downloading a file that doesn't exist"""
        response = self.client.get('/download/nonexistent_file.png')
        self.assertEqual(response.status_code, 404)

    def test_cleanup_old_files(self):
        """Test file cleanup functionality"""
        # Create some test files
        for i in range(15):
            test_file = os.path.join(self.test_output, f'test_{i}.png')
            with open(test_file, 'w') as f:
                f.write('test')

        # Set max files to 10
        original_max = self.app.config['MAX_OUTPUT_FILES']
        self.app.config['MAX_OUTPUT_FILES'] = 10

        # Run cleanup
        cleanup_old_files()

        # Check that files were removed
        remaining_files = [f for f in os.listdir(self.test_output) if f.endswith('.png')]
        self.assertLessEqual(len(remaining_files), 10)

        # Restore original max
        self.app.config['MAX_OUTPUT_FILES'] = original_max


if __name__ == '__main__':
    unittest.main()

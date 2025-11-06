"""
Tests for batch generation functionality
"""
import os
import sys
import unittest
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from batch_generator import (
    batch_generate_worksheets,
    batch_generate_all_formats_for_standard,
    BatchGenerationResult
)
from app import FORMAT_GENERATORS
from ngss_standards import NGSS_STANDARDS


class BatchGeneratorTests(unittest.TestCase):
    """Test batch generation functionality"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp(prefix='batch_test_')

        # Get test data
        self.test_standards = []
        for grade_level, standards in NGSS_STANDARDS.items():
            if standards:
                self.test_standards.append(standards[0])
                if len(self.test_standards) >= 2:
                    break

    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_batch_generation_result(self):
        """Test BatchGenerationResult object"""
        result = BatchGenerationResult()

        result.total = 5
        result.add_success({'test': 'success1'})
        result.add_success({'test': 'success2'})
        result.add_failure({'test': 'fail1'}, 'error message')
        result.complete()

        summary = result.summary()
        self.assertEqual(summary['total'], 5)
        self.assertEqual(summary['successful'], 2)
        self.assertEqual(summary['failed'], 1)
        self.assertIsNotNone(summary['duration_seconds'])

    def test_batch_generate_single_format(self):
        """Test batch generation with single format"""
        if not self.test_standards:
            self.skipTest("No test standards available")

        result = batch_generate_worksheets(
            FORMAT_GENERATORS,
            self.test_standards[:1],
            'K-2',
            ['crossword'],
            self.test_dir,
            max_workers=1
        )

        self.assertGreater(result.total, 0)
        self.assertEqual(len(result.successful), result.total)
        self.assertEqual(len(result.failed), 0)

        # Check files were created
        files = os.listdir(self.test_dir)
        self.assertGreater(len(files), 0)

    def test_batch_generate_multiple_formats(self):
        """Test batch generation with multiple formats"""
        if len(self.test_standards) < 1:
            self.skipTest("Not enough test standards")

        result = batch_generate_worksheets(
            FORMAT_GENERATORS,
            self.test_standards[:1],
            'K-2',
            ['crossword', 'word-search'],
            self.test_dir,
            max_workers=2
        )

        self.assertEqual(result.total, 2)
        self.assertGreater(len(result.successful), 0)

    def test_batch_generate_all_formats_for_standard(self):
        """Test generating all formats for a single standard"""
        if not self.test_standards:
            self.skipTest("No test standards available")

        result = batch_generate_all_formats_for_standard(
            FORMAT_GENERATORS,
            self.test_standards[0],
            'K-2',
            self.test_dir
        )

        self.assertGreater(result.total, 0)
        self.assertGreater(len(result.successful), 0)

        # Verify summary structure
        summary = result.summary()
        self.assertIn('total', summary)
        self.assertIn('successful', summary)
        self.assertIn('failed', summary)
        self.assertIn('success_rate', summary)

    def test_batch_generate_with_invalid_format(self):
        """Test batch generation with invalid format"""
        if not self.test_standards:
            self.skipTest("No test standards available")

        result = batch_generate_worksheets(
            FORMAT_GENERATORS,
            self.test_standards[:1],
            'K-2',
            ['nonexistent_format'],
            self.test_dir,
            max_workers=1
        )

        # Should handle gracefully
        self.assertEqual(result.total, 0)


if __name__ == '__main__':
    unittest.main()

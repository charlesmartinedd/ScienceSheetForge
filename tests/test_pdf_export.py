"""
Tests for PDF export functionality
"""
import os
import sys
import unittest
import tempfile
import shutil
from PIL import Image

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pdf_export import png_to_pdf, create_worksheet_bundle_pdf


class PDFExportTests(unittest.TestCase):
    """Test PDF export functionality"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp(prefix='pdf_test_')

    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def create_test_png(self, filename, size=(2550, 3300)):
        """Create a test PNG file"""
        img = Image.new('RGB', size, color='white')
        img.save(filename, 'PNG')
        return filename

    def test_png_to_pdf_conversion(self):
        """Test converting PNG to PDF"""
        png_path = os.path.join(self.test_dir, 'test.png')
        self.create_test_png(png_path)

        pdf_path = png_to_pdf(png_path)

        self.assertTrue(os.path.exists(pdf_path))
        self.assertTrue(pdf_path.endswith('.pdf'))
        self.assertGreater(os.path.getsize(pdf_path), 0)

    def test_png_to_pdf_with_custom_path(self):
        """Test PDF conversion with custom output path"""
        png_path = os.path.join(self.test_dir, 'test.png')
        pdf_path = os.path.join(self.test_dir, 'custom_output.pdf')

        self.create_test_png(png_path)
        result_path = png_to_pdf(png_path, pdf_path)

        self.assertEqual(result_path, pdf_path)
        self.assertTrue(os.path.exists(pdf_path))

    def test_png_to_pdf_nonexistent_file(self):
        """Test error handling for nonexistent PNG file"""
        with self.assertRaises(FileNotFoundError):
            png_to_pdf('nonexistent.png')

    def test_create_pdf_bundle(self):
        """Test creating multi-page PDF bundle"""
        png_files = []
        for i in range(3):
            png_path = os.path.join(self.test_dir, f'test_{i}.png')
            self.create_test_png(png_path)
            png_files.append(png_path)

        bundle_path = os.path.join(self.test_dir, 'bundle.pdf')
        result = create_worksheet_bundle_pdf(png_files, bundle_path)

        self.assertEqual(result, bundle_path)
        self.assertTrue(os.path.exists(bundle_path))
        self.assertGreater(os.path.getsize(bundle_path), 0)

    def test_create_pdf_bundle_empty_list(self):
        """Test error handling for empty file list"""
        with self.assertRaises(ValueError):
            create_worksheet_bundle_pdf([], 'output.pdf')

    def test_create_pdf_bundle_nonexistent_files(self):
        """Test error handling for nonexistent files"""
        with self.assertRaises(ValueError):
            create_worksheet_bundle_pdf(['nonexistent.png'], 'output.pdf')


if __name__ == '__main__':
    unittest.main()

import os
import shutil
import tempfile
import unittest

from app import AVAILABLE_FORMAT_IDS, FORMAT_GENERATORS
from ngss_standards import NGSS_STANDARDS


class GeneratorSmokeTests(unittest.TestCase):
    """Quick integration tests to ensure each available generator produces output."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix="sciencesheetforge-tests-")
        self.test_cases = []
        for grade_level, standards in NGSS_STANDARDS.items():
            if standards:
                self.test_cases.append((grade_level, standards[0]))
        self.assertTrue(
            self.test_cases,
            "NGSS standards list is empty; cannot run generator smoke tests."
        )

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_generate_all_formats(self):
        for fmt in sorted(AVAILABLE_FORMAT_IDS):
            for grade_level, standard in self.test_cases:
                case_label = f"{fmt}-{grade_level}-{standard['code']}"
                with self.subTest(case=case_label):
                    generator = FORMAT_GENERATORS.get(fmt)
                    self.assertTrue(callable(generator), f"Generator missing for format '{fmt}'")

                    output_path = os.path.join(self.tmp_dir, f"{fmt}_{grade_level}.png")
                    generator(standard, grade_level, output_path)

                    self.assertTrue(os.path.exists(output_path), "Worksheet file not created")
                    self.assertGreater(os.path.getsize(output_path), 0, "Worksheet file is empty")

                    answer_key_path = output_path.replace(".png", "_ANSWER_KEY.png")
                    self.assertTrue(os.path.exists(answer_key_path), "Answer key file not created")
                    self.assertGreater(os.path.getsize(answer_key_path), 0, "Answer key file is empty")


if __name__ == "__main__":
    unittest.main()

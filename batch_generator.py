"""
Batch Worksheet Generator for ScienceSheetForge
Generate multiple worksheets at once for different standards or formats
"""
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class BatchGenerationResult:
    """Result object for batch generation"""

    def __init__(self):
        self.successful = []
        self.failed = []
        self.total = 0
        self.start_time = datetime.now()
        self.end_time = None

    def add_success(self, item: Dict[str, Any]):
        """Add successful generation"""
        self.successful.append(item)

    def add_failure(self, item: Dict[str, Any], error: str):
        """Add failed generation"""
        self.failed.append({**item, 'error': error})

    def complete(self):
        """Mark batch as complete"""
        self.end_time = datetime.now()

    def duration(self):
        """Get generation duration"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def summary(self):
        """Get summary of batch generation"""
        return {
            'total': self.total,
            'successful': len(self.successful),
            'failed': len(self.failed),
            'duration_seconds': self.duration(),
            'success_rate': len(self.successful) / self.total if self.total > 0 else 0
        }

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'summary': self.summary(),
            'successful': self.successful,
            'failed': self.failed
        }


def generate_single_worksheet(generator_func, standard_data, grade_level, output_filename):
    """
    Generate a single worksheet (helper function for batch generation)

    Args:
        generator_func: Generator function to call
        standard_data: NGSS standard data
        grade_level: Grade level
        output_filename: Output file path

    Returns:
        Dict with generation info

    Raises:
        Exception: If generation fails
    """
    try:
        generator_func(standard_data, grade_level, output_filename)
        return {
            'standard': standard_data['code'],
            'grade_level': grade_level,
            'output_file': output_filename,
            'success': True
        }
    except Exception as e:
        logger.error(f"Failed to generate worksheet for {standard_data['code']}: {e}")
        raise


def batch_generate_worksheets(
    generator_dict: Dict,
    standards_list: List[Dict],
    grade_level: str,
    worksheet_formats: List[str],
    output_folder: str,
    max_workers: int = 4
) -> BatchGenerationResult:
    """
    Generate multiple worksheets in batch

    Args:
        generator_dict: Dictionary mapping format IDs to generator functions
        standards_list: List of NGSS standard data dictionaries
        grade_level: Grade level to generate for
        worksheet_formats: List of worksheet format IDs to generate
        output_folder: Output directory for worksheets
        max_workers: Maximum parallel workers (default: 4)

    Returns:
        BatchGenerationResult: Object containing results of batch generation

    Example:
        result = batch_generate_worksheets(
            FORMAT_GENERATORS,
            [standard1, standard2],
            'K-2',
            ['crossword', 'word-search'],
            'output/',
            max_workers=4
        )
    """
    result = BatchGenerationResult()

    # Create tasks list
    tasks = []
    for standard in standards_list:
        for fmt in worksheet_formats:
            if fmt not in generator_dict or not callable(generator_dict[fmt]):
                logger.warning(f"Skipping unavailable format: {fmt}")
                continue

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            output_filename = os.path.join(
                output_folder,
                f'{fmt}_{standard["code"]}_{timestamp}.png'
            )

            tasks.append({
                'generator': generator_dict[fmt],
                'standard': standard,
                'grade_level': grade_level,
                'output_filename': output_filename,
                'format': fmt
            })

    result.total = len(tasks)
    logger.info(f"Starting batch generation of {result.total} worksheets...")

    # Execute tasks in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_task = {
            executor.submit(
                generate_single_worksheet,
                task['generator'],
                task['standard'],
                task['grade_level'],
                task['output_filename']
            ): task
            for task in tasks
        }

        # Collect results
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                task_result = future.result()
                result.add_success({
                    'format': task['format'],
                    'standard': task['standard']['code'],
                    'output_file': task['output_filename'],
                    'answer_key': task['output_filename'].replace('.png', '_ANSWER_KEY.png')
                })
                logger.info(f"✓ Generated: {task['format']} - {task['standard']['code']}")
            except Exception as e:
                result.add_failure({
                    'format': task['format'],
                    'standard': task['standard']['code']
                }, str(e))
                logger.error(f"✗ Failed: {task['format']} - {task['standard']['code']}")

    result.complete()
    logger.info(f"Batch generation complete: {result.summary()}")

    return result


def batch_generate_all_formats_for_standard(
    generator_dict: Dict,
    standard_data: Dict,
    grade_level: str,
    output_folder: str
) -> BatchGenerationResult:
    """
    Generate all available worksheet formats for a single standard

    Args:
        generator_dict: Dictionary mapping format IDs to generator functions
        standard_data: NGSS standard data
        grade_level: Grade level
        output_folder: Output directory

    Returns:
        BatchGenerationResult: Object containing results
    """
    available_formats = [fmt for fmt, func in generator_dict.items() if callable(func)]

    return batch_generate_worksheets(
        generator_dict,
        [standard_data],
        grade_level,
        available_formats,
        output_folder
    )


if __name__ == '__main__':
    print("Batch Generator Module - Example Usage")
    print("=" * 50)
    print("Generate multiple worksheets:")
    print("  result = batch_generate_worksheets(")
    print("      FORMAT_GENERATORS,")
    print("      [standard1, standard2],")
    print("      'K-2',")
    print("      ['crossword', 'word-search'],")
    print("      'output/'")
    print("  )")
    print("\nCheck results:")
    print("  print(result.summary())")

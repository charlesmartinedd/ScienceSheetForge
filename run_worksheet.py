"""
Wrapper to run cell_hero_worksheet.py with proper encoding handling
"""
import sys
import os

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add examples directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples'))

# Import and run the worksheet generator
from cell_hero_worksheet import create_cell_hero_worksheet

if __name__ == "__main__":
    print("Cell Hero Worksheet Generator")
    print("=" * 50)

    # Generate a single worksheet
    create_cell_hero_worksheet()

    print("\nDone! Check your worksheet!")
    print("\nWorksheet saved in ScienceSheetForge directory")

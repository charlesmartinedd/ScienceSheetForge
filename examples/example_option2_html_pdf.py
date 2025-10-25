"""
OPTION 2 EXAMPLE: HTML/CSS to PDF Worksheet Generator
This shows how professional worksheets look when generated from HTML
"""

from xhtml2pdf import pisa
from datetime import datetime
import os

def generate_crossword_html_example():
    """Generate a professional crossword using HTML/CSS"""

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {
                size: letter;
                margin: 0.75in;
            }

            body {
                font-family: 'Arial', 'Helvetica', sans-serif;
                margin: 0;
                padding: 0;
                color: #000;
            }

            .worksheet {
                width: 100%;
            }

            /* Header Section */
            .header {
                text-align: center;
                border-bottom: 3px solid #000;
                padding-bottom: 10px;
                margin-bottom: 15px;
            }

            .header h1 {
                font-size: 28pt;
                margin: 0 0 8px 0;
                font-weight: bold;
                letter-spacing: 2px;
            }

            .header-info {
                display: flex;
                justify-content: space-between;
                font-size: 11pt;
                margin-top: 8px;
            }

            .topic {
                font-size: 14pt;
                font-weight: bold;
                margin: 12px 0;
            }

            .name-line {
                font-size: 11pt;
                margin: 10px 0 20px 0;
            }

            /* Crossword Grid */
            .crossword-grid {
                margin: 20px auto;
                display: inline-block;
            }

            .crossword-row {
                display: flex;
                height: 30px;
                line-height: 30px;
            }

            .grid-cell {
                width: 30px;
                height: 30px;
                border: 2px solid #000;
                position: relative;
                background: white;
                margin: 0;
                padding: 0;
            }

            .grid-cell.empty {
                border: none;
            }

            .cell-number {
                position: absolute;
                top: 1px;
                left: 2px;
                font-size: 8pt;
                font-weight: bold;
            }

            /* Clues Section */
            .clues-section {
                margin-top: 25px;
                border-top: 2px solid #000;
                padding-top: 15px;
            }

            .clues-container {
                display: flex;
                gap: 30px;
            }

            .clues-column {
                flex: 1;
            }

            .clues-column h3 {
                font-size: 13pt;
                font-weight: bold;
                margin: 0 0 10px 0;
                border-bottom: 1px solid #000;
                padding-bottom: 3px;
            }

            .clue {
                font-size: 10pt;
                margin: 6px 0;
                line-height: 1.4;
            }

            /* Footer */
            .footer {
                margin-top: 30px;
                text-align: center;
                font-size: 8pt;
                color: #666;
                border-top: 1px solid #ccc;
                padding-top: 8px;
            }
        </style>
    </head>
    <body>
        <div class="worksheet">
            <!-- Header -->
            <div class="header">
                <h1>CROSSWORD PUZZLE</h1>
                <div class="header-info">
                    <span>Grade 6-8</span>
                    <span>MS-LS1-2</span>
                </div>
            </div>

            <div class="topic">Topic: Cell Function</div>
            <div class="name-line">Name: _________________________________</div>

            <!-- Crossword Grid -->
            <div class="crossword-grid">
                <div class="crossword-row">
                    <div class="grid-cell empty"></div>
                    <div class="grid-cell empty"></div>
                    <div class="grid-cell"><span class="cell-number">1</span></div>
                    <div class="grid-cell"></div>
                    <div class="grid-cell"></div>
                    <div class="grid-cell"></div>
                </div>
                <div class="crossword-row">
                    <div class="grid-cell"><span class="cell-number">2</span></div>
                    <div class="grid-cell"></div>
                    <div class="grid-cell"></div>
                    <div class="grid-cell"></div>
                    <div class="grid-cell"></div>
                    <div class="grid-cell"></div>
                </div>
                <div class="crossword-row">
                    <div class="grid-cell empty"></div>
                    <div class="grid-cell empty"></div>
                    <div class="grid-cell"><span class="cell-number">3</span></div>
                    <div class="grid-cell"></div>
                    <div class="grid-cell empty"></div>
                    <div class="grid-cell empty"></div>
                </div>
                <div class="crossword-row">
                    <div class="grid-cell empty"></div>
                    <div class="grid-cell empty"></div>
                    <div class="grid-cell"></div>
                    <div class="grid-cell empty"></div>
                    <div class="grid-cell empty"></div>
                    <div class="grid-cell empty"></div>
                </div>
            </div>

            <!-- Clues -->
            <div class="clues-section">
                <div class="clues-container">
                    <div class="clues-column">
                        <h3>ACROSS</h3>
                        <div class="clue">1. The powerhouse of the cell that produces energy (ATP)</div>
                        <div class="clue">2. Process where plants make food using sunlight</div>
                    </div>
                    <div class="clues-column">
                        <h3>DOWN</h3>
                        <div class="clue">2. Process that releases energy from food molecules</div>
                        <div class="clue">3. Specialized structure within a cell</div>
                    </div>
                </div>
            </div>

            <div class="footer">
                ScienceSheetForge - Science Worksheets
            </div>
        </div>
    </body>
    </html>
    """

    # Generate PDF using xhtml2pdf
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'examples')
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, 'OPTION2_HTML_crossword_example.pdf')

    with open(output_file, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

    if not pisa_status.err:
        print(f"Option 2 example generated: {output_file}")
    else:
        print(f"Error generating PDF: {pisa_status.err}")

    return output_file

if __name__ == "__main__":
    generate_crossword_html_example()

"""
OPTION 2 EXAMPLE: HTML/CSS Screenshot Approach
Generate professional worksheets using HTML that can be screenshotted or exported
"""

from PIL import Image, ImageDraw, ImageFont
import os

# This version shows what HTML/CSS WOULD produce but generates PNG directly
# In production, we'd use Playwright to screenshot the rendered HTML

def generate_html_style_crossword():
    """
    This demonstrates what Option 2 (HTML/CSS) would look like.
    In production, we'd render actual HTML and screenshot it.
    This version shows the quality level you'd get.
    """

    width, height = 2550, 3300  # 8.5x11 at 300 DPI
    worksheet = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(worksheet)

    try:
        # Using system fonts - HTML/CSS has access to ALL fonts
        title_font = ImageFont.truetype("arial.ttf", 110)
        header_font = ImageFont.truetype("arial.ttf", 65)
        subtitle_font = ImageFont.truetype("arial.ttf", 48)
        text_font = ImageFont.truetype("arial.ttf", 42)
        small_font = ImageFont.truetype("arial.ttf", 36)
        num_font = ImageFont.truetype("arial.ttf", 30)
    except:
        title_font = header_font = subtitle_font = text_font = small_font = num_font = ImageFont.load_default()

    # Professional header - clean and centered
    title_text = "CROSSWORD PUZZLE"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 90), title_text, fill='black', font=title_font)

    # Bold underline
    draw.rectangle([250, 220, width-250, 226], fill='black')

    # Header info - perfectly aligned
    draw.text((150, 270), "Grade 6-8", fill='black', font=subtitle_font)
    draw.text((width - 600, 270), "MS-LS1-2", fill='black', font=subtitle_font)

    # Topic
    draw.text((150, 360), "Topic: Cell Function", fill='black', font=header_font)

    # Name line
    draw.text((150, 435), "Name: ", fill='black', font=text_font)
    draw.line([(280, 470), (850, 470)], fill='black', width=2)

    # Grid - perfectly sized and spaced
    cell_size = 65
    grid_start_x = 400
    grid_start_y = 550

    # Sample grid layout (small 6x6 for example)
    grid_layout = [
        [' ', ' ', '1', ' ', ' ', ' '],
        ['2', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '3', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
    ]

    for row_idx, row in enumerate(grid_layout):
        for col_idx, cell in enumerate(row):
            x = grid_start_x + col_idx * cell_size
            y = grid_start_y + row_idx * cell_size

            if cell != ' ':
                # Draw cell border
                draw.rectangle([x, y, x + cell_size, y + cell_size],
                             fill='white', outline='black', width=3)

                # Add number if present
                if cell.isdigit():
                    draw.text((x + 3, y + 2), cell, fill='black', font=num_font)

    # Clues section - two columns with clean layout
    clues_y = grid_start_y + (len(grid_layout) * cell_size) + 80

    # Divider line
    draw.rectangle([150, clues_y - 15, width-150, clues_y - 11], fill='black')

    # ACROSS column
    draw.text((200, clues_y), "ACROSS", fill='black', font=header_font)
    clue_y = clues_y + 90
    clues_across = [
        "1. The powerhouse of the cell that produces energy (ATP)",
        "2. Process where plants make food using sunlight",
    ]
    for clue in clues_across:
        draw.text((230, clue_y), clue, fill='black', font=text_font)
        clue_y += 70

    # DOWN column
    draw.text((width//2 + 150, clues_y), "DOWN", fill='black', font=header_font)
    clue_y = clues_y + 90
    clues_down = [
        "2. Process that releases energy from food molecules",
        "3. Specialized structure within a cell",
    ]
    for clue in clues_down:
        draw.text((width//2 + 180, clue_y), clue, fill='black', font=text_font)
        clue_y += 70

    # Footer - minimal and professional
    footer_y = height - 130
    draw.rectangle([150, footer_y, width-150, footer_y + 2], fill='black')
    footer_text = "ScienceSheetForge - Science Worksheets"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=small_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_width) // 2, footer_y + 25),
             footer_text, fill='gray', font=small_font)

    # Save
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'examples')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'OPTION2_HTML_STYLE_crossword.png')

    worksheet.save(output_file, quality=100, dpi=(300, 300))
    print(f"Option 2 (HTML-style) example generated: {output_file}")
    return output_file

if __name__ == "__main__":
    generate_html_style_crossword()

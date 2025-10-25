"""
WORD SEARCH - Teachers Pay Teachers Professional Style
Beautiful, sellable worksheets with decorative elements
"""

import random
from PIL import Image, ImageDraw, ImageFont


def draw_decorative_border(draw, width, height):
    """Add decorative border - TPT style"""
    border_color = '#2c3e50'
    margin = 50

    # Outer border
    draw.rectangle([margin, margin, width-margin, height-margin],
                   outline=border_color, width=8)

    # Inner border for depth
    draw.rectangle([margin+15, margin+15, width-margin-15, height-margin-15],
                   outline=border_color, width=3)

    # Corner decorations - small squares
    corner_size = 25
    for x, y in [(margin, margin), (width-margin-corner_size, margin),
                 (margin, height-margin-corner_size), (width-margin-corner_size, height-margin-corner_size)]:
        draw.rectangle([x, y, x+corner_size, y+corner_size], fill=border_color)


def draw_tpt_header(draw, width, standard_data, grade_level, fonts):
    """Draw beautiful TPT-style header"""
    title_font, header_font, subtitle_font = fonts

    # Decorative header box with gradient effect (simulated with rectangles)
    header_height = 280
    colors = ['#9b59b6', '#8e44ad', '#7d3c98']  # Purple gradient for word search

    for i, color in enumerate(colors):
        y_start = 80 + i * 30
        draw.rectangle([80, y_start, width-80, y_start + 30], fill=color)

    # Title - large and centered
    title_text = "WORD SEARCH"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 120), title_text, fill='white', font=title_font)

    # Decorative line under header
    draw.rectangle([100, header_height, width-100, header_height + 5], fill='#e67e22')

    # Info section - clean and organized
    info_y = header_height + 30
    draw.text((120, info_y), f"Grade: {grade_level}", fill='#2c3e50', font=subtitle_font)
    draw.text((width - 700, info_y), f"Standard: {standard_data['code']}",
             fill='#2c3e50', font=subtitle_font)

    # Topic in a nice box
    topic_y = info_y + 70
    draw.rectangle([100, topic_y, width-100, topic_y + 70],
                   fill='#ecf0f1', outline='#bdc3c7', width=3)
    topic_text = f"Topic: {standard_data['title']}"
    draw.text((120, topic_y + 15), topic_text, fill='#2c3e50', font=header_font)

    # Name line with decorative elements
    name_y = topic_y + 100
    draw.text((120, name_y), "Name:", fill='#2c3e50', font=subtitle_font)
    # Dotted line for name
    for x in range(300, width-120, 15):
        draw.line([(x, name_y + 45), (x+8, name_y + 45)], fill='#95a5a6', width=2)

    return name_y + 80


def generate_word_search(standard_data, grade_level, output_filename="word_search_tpt.png"):
    """Generate BEAUTIFUL TPT-style word search puzzle"""

    # Select 10-15 words
    vocabulary = standard_data['vocabulary']
    num_words = min(15, max(10, len(vocabulary)))
    selected_words = random.sample(vocabulary, num_words)
    selected_words = [w.upper() for w in selected_words if len(w) >= 3][:12]

    # Create grid
    grid_size = 15
    grid = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(grid_size)]
            for _ in range(grid_size)]

    # Place words
    placed_words = []
    for word in selected_words:
        attempts = 0
        while attempts < 50:
            direction = random.choice(['H', 'V', 'D'])  # Horizontal, Vertical, Diagonal
            if direction == 'H':
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - len(word))
                # Place word
                for i, letter in enumerate(word):
                    grid[row][col + i] = letter
                placed_words.append(word)
                break
            elif direction == 'V':
                row = random.randint(0, grid_size - len(word))
                col = random.randint(0, grid_size - 1)
                for i, letter in enumerate(word):
                    grid[row + i][col] = letter
                placed_words.append(word)
                break
            attempts += 1

    # CREATE BEAUTIFUL WORKSHEET
    width, height = 2550, 3300  # 8.5x11 at 300 DPI
    worksheet = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(worksheet)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 65)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 42)
        grid_font = ImageFont.truetype("arial.ttf", 38)
        small_font = ImageFont.truetype("arial.ttf", 38)
    except:
        title_font = header_font = subtitle_font = text_font = grid_font = small_font = ImageFont.load_default()

    # Add decorative border
    draw_decorative_border(draw, width, height)

    # Draw beautiful header
    grid_start_y = draw_tpt_header(draw, width, standard_data, grade_level,
                                   (title_font, header_font, subtitle_font))

    # WORD SEARCH GRID - Large and centered
    cell_size = 60
    grid_width = grid_size * cell_size
    grid_start_x = (width - grid_width) // 2

    # Grid background with subtle shadow
    shadow_offset = 6
    draw.rectangle([grid_start_x + shadow_offset, grid_start_y + shadow_offset,
                   grid_start_x + grid_width + shadow_offset, grid_start_y + (grid_size * cell_size) + shadow_offset],
                  fill='#bdc3c7')

    # Draw grid with letters
    for row in range(grid_size):
        for col in range(grid_size):
            x = grid_start_x + col * cell_size
            y = grid_start_y + row * cell_size

            # Cell with nice borders
            draw.rectangle([x, y, x + cell_size, y + cell_size],
                         fill='white', outline='#2c3e50', width=2)

            # Center letters in cells
            letter = grid[row][col]
            bbox = draw.textbbox((0, 0), letter, font=grid_font)
            letter_width = bbox[2] - bbox[0]
            letter_height = bbox[3] - bbox[1]
            draw.text((x + (cell_size - letter_width) // 2, y + (cell_size - letter_height) // 2 - 5),
                     letter, fill='#2c3e50', font=grid_font)

    # WORD LIST SECTION - Beautiful layout
    list_y = grid_start_y + (grid_size * cell_size) + 100

    # Decorative separator
    draw.rectangle([120, list_y - 30, width-120, list_y - 25], fill='#e67e22')

    # Word list header with styled box
    draw.rectangle([150, list_y, width-150, list_y + 70],
                   fill='#9b59b6', outline='#8e44ad', width=3)
    bbox = draw.textbbox((0, 0), "FIND THESE WORDS", font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, list_y + 10), "FIND THESE WORDS", fill='white', font=header_font)

    list_y += 110

    # Display words in 3 columns with checkboxes
    col_width = (width - 400) // 3
    for i, word in enumerate(placed_words):
        col_num = i % 3
        row_num = i // 3
        x_pos = 200 + col_num * col_width
        y_pos = list_y + row_num * 70

        # Checkbox
        checkbox_size = 30
        draw.rectangle([x_pos, y_pos + 5, x_pos + checkbox_size, y_pos + checkbox_size + 5],
                      fill='white', outline='#9b59b6', width=3)

        # Word
        draw.text((x_pos + checkbox_size + 15, y_pos), word.title(), fill='#2c3e50', font=text_font)

    # FOOTER with branding
    footer_y = height - 100
    draw.rectangle([120, footer_y - 10, width-120, footer_y + 60],
                   fill='#ecf0f1', outline='#bdc3c7', width=2)
    footer_text = "ScienceSheetForge - Premium Science Worksheets"
    bbox = draw.textbbox((0, 0), footer_text, font=small_font)
    footer_width = bbox[2] - bbox[0]
    draw.text(((width - footer_width) // 2, footer_y + 5),
             footer_text, fill='#7f8c8d', font=small_font)

    worksheet.save(output_filename, quality=100, dpi=(300, 300))
    print(f"TPT-Style word search saved: {output_filename}")

    # Generate answer key
    generate_word_search_answer_key(grid, grid_size, standard_data, placed_words, grade_level,
                                    output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_word_search_answer_key(grid, grid_size, standard_data, words, grade_level, output_filename):
    """Generate beautiful TPT-style answer key"""

    width, height = 2550, 3300  # 8.5x11 at 300 DPI
    answer_key = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(answer_key)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 65)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 42)
        small_font = ImageFont.truetype("arial.ttf", 38)
    except:
        title_font = header_font = subtitle_font = text_font = small_font = ImageFont.load_default()

    # Add decorative border
    draw_decorative_border(draw, width, height)

    # Purple gradient header for answer key
    header_height = 280
    colors = ['#9b59b6', '#8e44ad', '#7d3c98']

    for i, color in enumerate(colors):
        y_start = 80 + i * 30
        draw.rectangle([80, y_start, width-80, y_start + 30], fill=color)

    # Title - large and centered
    title_text = "ANSWER KEY"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 120), title_text, fill='white', font=title_font)

    # Decorative line under header
    draw.rectangle([100, header_height, width-100, header_height + 5], fill='#e67e22')

    # Info section
    info_y = header_height + 30
    draw.text((120, info_y), f"Grade: {grade_level}", fill='#2c3e50', font=subtitle_font)
    draw.text((width - 700, info_y), f"Standard: {standard_data['code']}",
             fill='#2c3e50', font=subtitle_font)

    # Word list section
    list_y = info_y + 100

    # Decorative separator
    draw.rectangle([120, list_y - 20, width-120, list_y - 15], fill='#e67e22')

    # Header
    draw.rectangle([150, list_y, width-150, list_y + 70],
                   fill='#27ae60', outline='#229954', width=3)
    bbox = draw.textbbox((0, 0), "WORDS IN PUZZLE", font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, list_y + 10), "WORDS IN PUZZLE", fill='white', font=header_font)

    list_y += 110

    # Display words in 3 columns with checkmarks
    col_width = (width - 400) // 3
    for i, word in enumerate(words):
        col_num = i % 3
        row_num = i // 3
        x_pos = 200 + col_num * col_width
        y_pos = list_y + row_num * 70

        # Checkmark circle
        draw.ellipse([x_pos, y_pos, x_pos + 40, y_pos + 40],
                    fill='#27ae60', outline='#229954', width=2)
        draw.text((x_pos + 10, y_pos + 5), "V", fill='white', font=text_font)

        # Word
        draw.text((x_pos + 55, y_pos + 3), word.upper(), fill='#2c3e50', font=text_font)

    # FOOTER with branding
    footer_y = height - 100
    draw.rectangle([120, footer_y - 10, width-120, footer_y + 60],
                   fill='#ecf0f1', outline='#bdc3c7', width=2)
    footer_text = "ScienceSheetForge - Premium Science Worksheets"
    bbox = draw.textbbox((0, 0), footer_text, font=small_font)
    footer_width = bbox[2] - bbox[0]
    draw.text(((width - footer_width) // 2, footer_y + 5),
             footer_text, fill='#7f8c8d', font=small_font)

    answer_key.save(output_filename, quality=100, dpi=(300, 300))
    print(f"TPT-Style answer key saved: {output_filename}")


if __name__ == "__main__":
    # Test with sample data
    sample_standard = {
        'code': 'MS-LS1-2',
        'title': 'Cell Function',
        'vocabulary': ['cell', 'nucleus', 'mitochondria', 'chloroplast', 'ribosome',
                      'membrane', 'cytoplasm', 'vacuole', 'organism', 'tissue',
                      'organ', 'system', 'dna', 'protein', 'energy']
    }

    generate_word_search(sample_standard, "6-8", "output/examples/OPTION4_TPT_STYLE_word_search.png")

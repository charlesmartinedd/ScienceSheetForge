"""
Smart Word Search Generator
Uses intelligent content engine for TPT-quality worksheets
"""

import random
import sys
import os
from PIL import Image, ImageDraw, ImageFont

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ai_engine.smart_content import get_smart_content


def draw_decorative_border(draw, width, height):
    """Add decorative border - TPT style"""
    border_color = '#2c3e50'
    margin = 50

    draw.rectangle([margin, margin, width-margin, height-margin],
                   outline=border_color, width=8)
    draw.rectangle([margin+15, margin+15, width-margin-15, height-margin-15],
                   outline=border_color, width=3)

    corner_size = 25
    for x, y in [(margin, margin), (width-margin-corner_size, margin),
                 (margin, height-margin-corner_size), (width-margin-corner_size, height-margin-corner_size)]:
        draw.rectangle([x, y, x+corner_size, y+corner_size], fill=border_color)


def draw_tpt_header(draw, width, standard_data, grade_level, fonts):
    """Draw beautiful TPT-style header"""
    title_font, header_font, subtitle_font = fonts

    header_height = 280
    colors = ['#9b59b6', '#8e44ad', '#7d3c98']  # Purple gradient

    for i, color in enumerate(colors):
        y_start = 80 + i * 30
        draw.rectangle([80, y_start, width-80, y_start + 30], fill=color)

    title_text = "WORD SEARCH"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 120), title_text, fill='white', font=title_font)

    draw.rectangle([100, header_height, width-100, header_height + 5], fill='#e67e22')

    info_y = header_height + 30
    draw.text((120, info_y), f"Grade: {grade_level}", fill='#2c3e50', font=subtitle_font)
    draw.text((width - 700, info_y), f"Standard: {standard_data['code']}", fill='#2c3e50', font=subtitle_font)

    topic_y = info_y + 70
    draw.rectangle([100, topic_y, width-100, topic_y + 70],
                   fill='#ecf0f1', outline='#bdc3c7', width=3)
    topic_text = f"Topic: {standard_data['title']}"
    draw.text((120, topic_y + 15), topic_text, fill='#2c3e50', font=header_font)

    name_y = topic_y + 100
    draw.text((120, name_y), "Name:", fill='#2c3e50', font=subtitle_font)
    for x in range(300, width-120, 15):
        draw.line([(x, name_y + 45), (x+8, name_y + 45)], fill='#95a5a6', width=2)

    return name_y + 80


def generate_word_search(standard_data, grade_level, output_filename="word_search.png"):
    """Generate smart TPT-style word search"""

    print(f"Generating smart word search for {standard_data['code']}...")

    # Get smart content engine
    content = get_smart_content()

    # Generate vocabulary
    print("   Generating vocabulary...")
    vocabulary = content.generate_vocabulary_words(
        standard_data['title'],
        count=15,
        vocabulary_pool=standard_data.get('vocabulary'),
        topics=standard_data.get('topics'),
    )

    # Select 10-12 words for word search
    selected_words = [w for w in vocabulary if len(w) >= 3][:12]
    selected_words = [w.upper() for w in selected_words]

    print(f"   Generated {len(selected_words)} words for word search")

    # Create grid
    grid_size = 15
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

    def can_place(word_to_place, row_idx, col_idx, direction):
        for offset, letter in enumerate(word_to_place):
            r, c = row_idx, col_idx
            if direction == 'H':
                c += offset
            elif direction == 'V':
                r += offset
            else:  # Diagonal
                r += offset
                c += offset

            if r >= grid_size or c >= grid_size:
                return False

            existing = grid[r][c]
            if existing not in (' ', letter):
                return False
        return True

    def place_word(word_to_place, row_idx, col_idx, direction):
        for offset, letter in enumerate(word_to_place):
            r, c = row_idx, col_idx
            if direction == 'H':
                c += offset
            elif direction == 'V':
                r += offset
            else:
                r += offset
                c += offset
            grid[r][c] = letter

    directions = ['H', 'V', 'D']
    placed_words = []
    for word in selected_words:
        placed = False
        for _ in range(100):
            direction = random.choice(directions)
            if direction == 'H':
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - len(word))
            elif direction == 'V':
                row = random.randint(0, grid_size - len(word))
                col = random.randint(0, grid_size - 1)
            else:
                row = random.randint(0, grid_size - len(word))
                col = random.randint(0, grid_size - len(word))

            if can_place(word, row, col, direction):
                place_word(word, row, col, direction)
                placed_words.append(word)
                placed = True
                break

        if not placed:
            print(f"   Warning: could not place '{word}' in word search grid")

    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] == ' ':
                grid[row][col] = random.choice(alphabet)

    print(f"   Placed {len(placed_words)} words in grid")

    # CREATE WORKSHEET
    width, height = 2550, 3300
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

    draw_decorative_border(draw, width, height)
    grid_start_y = draw_tpt_header(draw, width, standard_data, grade_level,
                                   (title_font, header_font, subtitle_font))

    # GRID
    cell_size = 60
    grid_width = grid_size * cell_size
    grid_start_x = (width - grid_width) // 2

    shadow_offset = 6
    draw.rectangle([grid_start_x + shadow_offset, grid_start_y + shadow_offset,
                   grid_start_x + grid_width + shadow_offset, grid_start_y + (grid_size * cell_size) + shadow_offset],
                  fill='#bdc3c7')

    for row in range(grid_size):
        for col in range(grid_size):
            x = grid_start_x + col * cell_size
            y = grid_start_y + row * cell_size

            draw.rectangle([x, y, x + cell_size, y + cell_size],
                         fill='white', outline='#2c3e50', width=2)

            letter = grid[row][col]
            bbox = draw.textbbox((0, 0), letter, font=grid_font)
            letter_width = bbox[2] - bbox[0]
            letter_height = bbox[3] - bbox[1]
            draw.text((x + (cell_size - letter_width) // 2, y + (cell_size - letter_height) // 2 - 5),
                     letter, fill='#2c3e50', font=grid_font)

    # WORD LIST
    list_y = grid_start_y + (grid_size * cell_size) + 100
    draw.rectangle([120, list_y - 30, width-120, list_y - 25], fill='#e67e22')

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

        checkbox_size = 30
        draw.rectangle([x_pos, y_pos + 5, x_pos + checkbox_size, y_pos + checkbox_size + 5],
                      fill='white', outline='#9b59b6', width=3)

        draw.text((x_pos + checkbox_size + 15, y_pos), word.title(), fill='#2c3e50', font=text_font)

    rows_used = (len(placed_words) + 2) // 3
    fun_fact_y = list_y + rows_used * 70 + 120

    fun_facts = []
    for word in placed_words:
        fact = content.get_fun_fact(word)
        if fact:
            fun_facts.append((word.title(), fact))
    fun_facts = fun_facts[:3]

    if fun_facts:
        draw.rectangle([150, fun_fact_y - 30, width-150, fun_fact_y - 25], fill='#9b59b6')
        draw.rectangle([150, fun_fact_y, width-150, fun_fact_y + 90],
                       fill='#ecf0f1', outline='#8e44ad', width=3)
        bbox = draw.textbbox((0, 0), "Did You Know?", font=header_font)
        title_width = bbox[2] - bbox[0]
        draw.text(((width - title_width) // 2, fun_fact_y + 15), "Did You Know?", fill='#2c3e50', font=header_font)

        fact_text_y = fun_fact_y + 120
        for word_title, fact in fun_facts:
            full_text = f"{word_title}: {fact}"
            words = full_text.split()
            current_line = []
            for token in words:
                test_line = ' '.join(current_line + [token])
                bbox = draw.textbbox((0, 0), test_line, font=small_font)
                if bbox[2] - bbox[0] <= (width - 360):
                    current_line.append(token)
                else:
                    draw.text((180, fact_text_y), ' '.join(current_line), fill='#2c3e50', font=small_font)
                    fact_text_y += 55
                    current_line = [token]
            if current_line:
                draw.text((180, fact_text_y), ' '.join(current_line), fill='#2c3e50', font=small_font)
                fact_text_y += 80

    # FOOTER
    footer_y = height - 100
    draw.rectangle([120, footer_y - 10, width-120, footer_y + 60],
                   fill='#ecf0f1', outline='#bdc3c7', width=2)
    footer_text = "ScienceSheetForge - Smart Science Worksheets"
    bbox = draw.textbbox((0, 0), footer_text, font=small_font)
    footer_width = bbox[2] - bbox[0]
    draw.text(((width - footer_width) // 2, footer_y + 5),
             footer_text, fill='#7f8c8d', font=small_font)

    worksheet.save(output_filename, quality=100, dpi=(300, 300))
    print(f"Smart word search saved: {output_filename}")

    # Generate answer key
    generate_answer_key(placed_words, standard_data, grade_level,
                       output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_answer_key(words, standard_data, grade_level, output_filename):
    """Generate answer key with word list"""
    width, height = 2550, 3300
    answer_key = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(answer_key)
    content = get_smart_content()

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 65)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 42)
        small_font = ImageFont.truetype("arial.ttf", 38)
    except:
        title_font = header_font = subtitle_font = text_font = small_font = ImageFont.load_default()

    draw_decorative_border(draw, width, height)

    header_height = 280
    colors = ['#27ae60', '#229954', '#1e8449']

    for i, color in enumerate(colors):
        y_start = 80 + i * 30
        draw.rectangle([80, y_start, width-80, y_start + 30], fill=color)

    title_text = "ANSWER KEY"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 120), title_text, fill='white', font=title_font)

    draw.rectangle([100, header_height, width-100, header_height + 5], fill='#e67e22')

    info_y = header_height + 30
    draw.text((120, info_y), f"Grade: {grade_level}", fill='#2c3e50', font=subtitle_font)
    draw.text((width - 700, info_y), f"Standard: {standard_data['code']}", fill='#2c3e50', font=subtitle_font)

    list_y = info_y + 100
    draw.rectangle([120, list_y - 20, width-120, list_y - 15], fill='#e67e22')

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

        draw.ellipse([x_pos, y_pos, x_pos + 40, y_pos + 40],
                    fill='#27ae60', outline='#229954', width=2)
        draw.text((x_pos + 10, y_pos + 5), "V", fill='white', font=text_font)

        draw.text((x_pos + 55, y_pos + 3), word.upper(), fill='#2c3e50', font=text_font)

    rows_used = (len(words) + 2) // 3
    fun_fact_y = list_y + rows_used * 70 + 120

    fun_facts = []
    for word in words:
        fact = content.get_fun_fact(word)
        if fact:
            fun_facts.append((word.title(), fact))
    fun_facts = fun_facts[:3]

    if fun_facts:
        draw.rectangle([150, fun_fact_y - 30, width-150, fun_fact_y - 25], fill='#27ae60')
        draw.rectangle([150, fun_fact_y, width-150, fun_fact_y + 90],
                       fill='#ecf0f1', outline='#229954', width=3)
        bbox = draw.textbbox((0, 0), "Fun Science Facts", font=header_font)
        title_width = bbox[2] - bbox[0]
        draw.text(((width - title_width) // 2, fun_fact_y + 15), "Fun Science Facts", fill='#2c3e50', font=header_font)

        fact_text_y = fun_fact_y + 120
        for word_title, fact in fun_facts:
            full_text = f"{word_title}: {fact}"
            words = full_text.split()
            current_line = []
            for token in words:
                test_line = ' '.join(current_line + [token])
                bbox = draw.textbbox((0, 0), test_line, font=small_font)
                if bbox[2] - bbox[0] <= (width - 360):
                    current_line.append(token)
                else:
                    draw.text((180, fact_text_y), ' '.join(current_line), fill='#2c3e50', font=small_font)
                    fact_text_y += 55
                    current_line = [token]
            if current_line:
                draw.text((180, fact_text_y), ' '.join(current_line), fill='#2c3e50', font=small_font)
                fact_text_y += 80

    # FOOTER
    footer_y = height - 100
    draw.rectangle([120, footer_y - 10, width-120, footer_y + 60],
                   fill='#ecf0f1', outline='#bdc3c7', width=2)
    footer_text = "ScienceSheetForge - Smart Science Worksheets"
    bbox = draw.textbbox((0, 0), footer_text, font=small_font)
    footer_width = bbox[2] - bbox[0]
    draw.text(((width - footer_width) // 2, footer_y + 5),
             footer_text, fill='#7f8c8d', font=small_font)

    answer_key.save(output_filename, quality=100, dpi=(300, 300))
    print(f"Answer key saved: {output_filename}")


if __name__ == "__main__":
    sample_standard = {
        'code': 'MS-LS1-2',
        'title': 'Cell Function and Processes',
        'vocabulary': ['cell', 'nucleus', 'mitochondria']
    }

    generate_word_search(sample_standard, "6-8", "output/test_smart_word_search.png")

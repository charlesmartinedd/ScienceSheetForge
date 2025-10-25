"""
Smart Crossword Generator
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
    colors = ['#3498db', '#2980b9', '#21618c']

    for i, color in enumerate(colors):
        y_start = 80 + i * 30
        draw.rectangle([80, y_start, width-80, y_start + 30], fill=color)

    title_text = "CROSSWORD PUZZLE"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 120), title_text, fill='white', font=title_font)

    draw.rectangle([100, header_height, width-100, header_height + 5], fill='#f39c12')

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


def generate_crossword_tpt_style(standard_data, grade_level, output_filename="crossword.png"):
    """Generate smart TPT-style crossword"""

    print(f"Generating smart crossword for {standard_data['code']}...")

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

    # Generate clues
    print("   Generating smart clues...")
    clues_dict = {}
    for word in vocabulary[:10]:
        clue = content.generate_crossword_clue(word, grade_level, difficulty="medium")
        clues_dict[word] = clue

    selected_words = list(clues_dict.keys())[:10]
    selected_words.sort(key=len, reverse=True)

    print(f"   Generated {len(selected_words)} words with smart clues")

    # Simple placement algorithm
    grid_size = 15
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    placements = []

    first_word = selected_words[0].upper()
    start_row = grid_size // 2
    start_col = (grid_size - len(first_word)) // 2

    for i, letter in enumerate(first_word):
        grid[start_row][start_col + i] = letter

    placements.append({
        'word': selected_words[0],
        'row': start_row,
        'col': start_col,
        'direction': 'across',
        'number': 1
    })

    # Place more words
    word_num = 2
    for word in selected_words[1:8]:
        word_upper = word.upper()
        placed = False

        for existing in placements[:]:
            if placed:
                break
            for i, letter in enumerate(word_upper):
                existing_word = existing['word'].upper()
                for j, ex_letter in enumerate(existing_word):
                    if letter == ex_letter:
                        if existing['direction'] == 'across':
                            new_row = existing['row'] - i
                            new_col = existing['col'] + j

                            if new_row >= 0 and new_row + len(word_upper) <= grid_size:
                                can_place = all(
                                    grid[new_row + k][new_col] in [' ', word_upper[k]]
                                    for k in range(len(word_upper))
                                )

                                if can_place:
                                    for k, l in enumerate(word_upper):
                                        grid[new_row + k][new_col] = l

                                    placements.append({
                                        'word': word,
                                        'row': new_row,
                                        'col': new_col,
                                        'direction': 'down',
                                        'number': word_num
                                    })
                                    word_num += 1
                                    placed = True
                                    break
                        else:
                            new_row = existing['row'] + j
                            new_col = existing['col'] - i

                            if new_col >= 0 and new_col + len(word_upper) <= grid_size:
                                can_place = all(
                                    grid[new_row][new_col + k] in [' ', word_upper[k]]
                                    for k in range(len(word_upper))
                                )

                                if can_place:
                                    for k, l in enumerate(word_upper):
                                        grid[new_row][new_col + k] = l

                                    placements.append({
                                        'word': word,
                                        'row': new_row,
                                        'col': new_col,
                                        'direction': 'across',
                                        'number': word_num
                                    })
                                    word_num += 1
                                    placed = True
                                    break
                if placed:
                    break

        if not placed:
            print(f"   Warning: could not place '{word}' in crossword grid")

    print(f"   Placed {len(placements)} words in grid")

    # CREATE WORKSHEET
    width, height = 2550, 3300
    worksheet = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(worksheet)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 65)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 42)
        small_font = ImageFont.truetype("arial.ttf", 38)
        num_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = header_font = subtitle_font = text_font = small_font = num_font = ImageFont.load_default()

    draw_decorative_border(draw, width, height)
    grid_start_y = draw_tpt_header(draw, width, standard_data, grade_level,
                                   (title_font, header_font, subtitle_font))

    # GRID
    cell_size = 65
    grid_width = grid_size * cell_size
    grid_start_x = (width - grid_width) // 2

    shadow_offset = 6
    draw.rectangle([grid_start_x + shadow_offset, grid_start_y + shadow_offset,
                   grid_start_x + grid_width + shadow_offset, grid_start_y + (grid_size * cell_size) + shadow_offset],
                  fill='#bdc3c7')

    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] != ' ':
                x = grid_start_x + col * cell_size
                y = grid_start_y + row * cell_size
                draw.rectangle([x, y, x + cell_size, y + cell_size],
                             fill='white', outline='#2c3e50', width=3)

    for placement in placements:
        x = grid_start_x + placement['col'] * cell_size
        y = grid_start_y + placement['row'] * cell_size
        draw.ellipse([x+2, y+2, x+22, y+22], fill='#3498db')
        draw.text((x + 7, y + 2), str(placement['number']), fill='white', font=num_font)

    # CLUES
    clues_y = grid_start_y + (grid_size * cell_size) + 100
    draw.rectangle([120, clues_y - 30, width-120, clues_y - 25], fill='#f39c12')

    across_x = 150
    draw.rectangle([across_x - 20, clues_y, across_x + 500, clues_y + 60],
                   fill='#3498db', outline='#2980b9', width=3)
    draw.text((across_x + 150, clues_y + 10), "ACROSS", fill='white', font=header_font)

    clues_y += 90
    across_clues = [p for p in placements if p['direction'] == 'across']
    for placement in across_clues[:5]:
        clue = clues_dict.get(placement['word'], "Science term")
        if len(clue) > 55:
            clue = clue[:55] + "..."

        draw.ellipse([across_x, clues_y, across_x + 35, clues_y + 35], fill='#ecf0f1', outline='#3498db', width=2)
        draw.text((across_x + 10, clues_y + 5), str(placement['number']), fill='#2c3e50', font=text_font)
        draw.text((across_x + 50, clues_y + 5), clue, fill='#2c3e50', font=text_font)
        clues_y += 65

    down_x = width // 2 + 100
    clues_y = grid_start_y + (grid_size * cell_size) + 100

    draw.rectangle([down_x - 20, clues_y, down_x + 450, clues_y + 60],
                   fill='#27ae60', outline='#229954', width=3)
    draw.text((down_x + 140, clues_y + 10), "DOWN", fill='white', font=header_font)

    clues_y += 90
    down_clues = [p for p in placements if p['direction'] == 'down']
    for placement in down_clues[:5]:
        clue = clues_dict.get(placement['word'], "Science term")
        if len(clue) > 50:
            clue = clue[:50] + "..."

        draw.ellipse([down_x, clues_y, down_x + 35, clues_y + 35], fill='#ecf0f1', outline='#27ae60', width=2)
        draw.text((down_x + 10, clues_y + 5), str(placement['number']), fill='#2c3e50', font=text_font)
        draw.text((down_x + 50, clues_y + 5), clue, fill='#2c3e50', font=text_font)
        clues_y += 65

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
    print(f"Smart crossword saved: {output_filename}")

    # Generate answer key
    generate_answer_key(grid, grid_size, standard_data, placements, grade_level,
                       output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_answer_key(grid, grid_size, standard_data, placements, grade_level, output_filename):
    """Generate answer key"""
    width, height = 2550, 3300
    answer_key = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(answer_key)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 65)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        grid_font = ImageFont.truetype("arial.ttf", 38)
        small_font = ImageFont.truetype("arial.ttf", 38)
    except:
        title_font = header_font = subtitle_font = grid_font = small_font = ImageFont.load_default()

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

    draw.rectangle([100, header_height, width-100, header_height + 5], fill='#f39c12')

    info_y = header_height + 30
    draw.text((120, info_y), f"Grade: {grade_level}", fill='#2c3e50', font=subtitle_font)
    draw.text((width - 700, info_y), f"Standard: {standard_data['code']}", fill='#2c3e50', font=subtitle_font)

    grid_start_y = info_y + 100

    cell_size = 65
    grid_width = grid_size * cell_size
    grid_start_x = (width - grid_width) // 2

    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] != ' ':
                x = grid_start_x + col * cell_size
                y = grid_start_y + row * cell_size

                draw.rectangle([x, y, x + cell_size, y + cell_size],
                             fill='#d4edda', outline='#27ae60', width=3)

                letter = grid[row][col]
                bbox = draw.textbbox((0, 0), letter, font=grid_font)
                letter_width = bbox[2] - bbox[0]
                letter_height = bbox[3] - bbox[1]
                draw.text((x + (cell_size - letter_width) // 2, y + (cell_size - letter_height) // 2 - 5),
                         letter, fill='#27ae60', font=grid_font)

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

    generate_crossword_tpt_style(sample_standard, "6-8", "output/test_smart_crossword.png")

"""
Smart True/False Quiz Generator
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
    colors = ['#16a085', '#138d75', '#117a65']  # Teal gradient

    for i, color in enumerate(colors):
        y_start = 80 + i * 30
        draw.rectangle([80, y_start, width-80, y_start + 30], fill=color)

    title_text = "TRUE or FALSE"
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


def generate_true_false(standard_data, grade_level, output_filename="true_false.png"):
    """Generate smart TPT-style true/false quiz"""

    print(f"Generating true/false quiz for {standard_data['code']}...")

    # Get smart content engine
    content = get_smart_content()

    # Generate vocabulary
    print("   Generating statements...")
    vocabulary = content.generate_vocabulary_words(
        standard_data['title'],
        count=15,
        vocabulary_pool=standard_data.get('vocabulary'),
        topics=standard_data.get('topics'),
    )

    # Create true/false statements
    statements = []

    for word in vocabulary[:10]:
        definition = content.get_definition(word, grade_level)

        # Create true statement
        if grade_level == "K-2":
            true_statement = f"A {word.lower()} is {definition.lower()}"
        else:
            true_statement = f"The {word.lower()} is {definition.lower()}"

        is_true = random.choice([True, False])

        if is_true:
            statements.append((true_statement, True))
        else:
            # Create false statement by swapping with another word
            other_words = [w for w in vocabulary[:10] if w != word]
            if other_words:
                wrong_word = random.choice(other_words)
                wrong_def = content.get_definition(wrong_word, grade_level)

                if grade_level == "K-2":
                    false_statement = f"A {word.lower()} is {wrong_def.lower()}"
                else:
                    false_statement = f"The {word.lower()} is {wrong_def.lower()}"

                statements.append((false_statement, False))
            else:
                statements.append((true_statement, True))

    # Shuffle statements
    random.shuffle(statements)

    print(f"   Generated {len(statements)} true/false statements")

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
    except:
        title_font = header_font = subtitle_font = text_font = small_font = ImageFont.load_default()

    draw_decorative_border(draw, width, height)
    content_start_y = draw_tpt_header(draw, width, standard_data, grade_level,
                                      (title_font, header_font, subtitle_font))

    # Instructions box
    instructions_y = content_start_y
    draw.rectangle([120, instructions_y, width-120, instructions_y + 80],
                   fill='#fff3cd', outline='#ffc107', width=3)
    draw.text((140, instructions_y + 15),
             "Directions: Circle TRUE if the statement is correct, or FALSE if it is incorrect.",
             fill='#2c3e50', font=text_font)

    # Statements section
    statements_y = instructions_y + 120
    draw.rectangle([120, statements_y - 30, width-120, statements_y - 25], fill='#e67e22')

    for i, (statement, answer) in enumerate(statements):
        statement_y = statements_y + i * 250

        # Number in circle
        draw.ellipse([140, statement_y, 200, statement_y + 60], fill='#16a085')
        draw.text((158, statement_y + 10), str(i+1), fill='white', font=header_font)

        # Statement box
        draw.rectangle([220, statement_y - 10, width-140, statement_y + 120],
                      fill='#e8f8f5', outline='#16a085', width=3)

        # Wrap statement text
        words = statement.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=small_font)
            if bbox[2] - bbox[0] < 2100:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Draw statement
        for j, line in enumerate(lines[:3]):
            draw.text((240, statement_y + j * 45), line, fill='#2c3e50', font=small_font)

        # TRUE/FALSE buttons
        buttons_y = statement_y + 150

        # TRUE button
        draw.rectangle([250, buttons_y, 600, buttons_y + 70],
                      fill='white', outline='#27ae60', width=4)
        draw.text((360, buttons_y + 15), "TRUE", fill='#27ae60', font=header_font)

        # FALSE button
        draw.rectangle([650, buttons_y, 1000, buttons_y + 70],
                      fill='white', outline='#e74c3c', width=4)
        draw.text((740, buttons_y + 15), "FALSE", fill='#e74c3c', font=header_font)

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
    print(f"True/false quiz saved: {output_filename}")

    # Generate answer key
    generate_answer_key(statements, standard_data, grade_level,
                       output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_answer_key(statements, standard_data, grade_level, output_filename):
    """Generate answer key"""
    width, height = 2550, 3300
    answer_key = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(answer_key)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 65)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 45)
        small_font = ImageFont.truetype("arial.ttf", 38)
    except:
        title_font = header_font = subtitle_font = text_font = small_font = ImageFont.load_default()

    draw_decorative_border(draw, width, height)

    # Header
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

    # Answers section
    list_y = info_y + 100
    draw.rectangle([120, list_y - 20, width-120, list_y - 15], fill='#e67e22')

    draw.rectangle([150, list_y, width-150, list_y + 70],
                   fill='#27ae60', outline='#229954', width=3)
    bbox = draw.textbbox((0, 0), "CORRECT ANSWERS", font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, list_y + 10), "CORRECT ANSWERS", fill='white', font=header_font)

    list_y += 110

    # Display answers in a compact format
    col_width = (width - 400) // 2

    for i, (statement, answer) in enumerate(statements):
        col_num = i % 2
        row_num = i // 2
        x_pos = 200 + col_num * col_width
        y_pos = list_y + row_num * 100

        # Answer box
        draw.rectangle([x_pos, y_pos - 5, x_pos + 1000, y_pos + 70],
                      fill='#d4edda', outline='#27ae60', width=3)

        # Number
        draw.ellipse([x_pos + 20, y_pos + 10, x_pos + 70, y_pos + 60], fill='#16a085')
        draw.text((x_pos + 35, y_pos + 15), str(i+1), fill='white', font=text_font)

        # Answer
        answer_text = "TRUE" if answer else "FALSE"
        answer_color = '#27ae60' if answer else '#e74c3c'

        draw.rectangle([x_pos + 100, y_pos + 10, x_pos + 350, y_pos + 60],
                      fill=answer_color, outline='#2c3e50', width=2)
        bbox = draw.textbbox((0, 0), answer_text, font=text_font)
        text_width = bbox[2] - bbox[0]
        draw.text((x_pos + 225 - text_width // 2, y_pos + 15), answer_text, fill='white', font=text_font)

        # Checkmark
        draw.ellipse([x_pos + 380, y_pos + 15, x_pos + 430, y_pos + 65],
                    fill='#27ae60', outline='#229954', width=2)
        draw.text((x_pos + 393, y_pos + 17), "V", fill='white', font=text_font)

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

    generate_true_false(sample_standard, "6-8", "output/test_true_false.png")

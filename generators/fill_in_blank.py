"""
Smart Fill-in-the-Blank Generator
Uses intelligent content engine for TPT-quality worksheets
"""

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
    colors = ['#f39c12', '#e67e22', '#d35400']  # Orange gradient

    for i, color in enumerate(colors):
        y_start = 80 + i * 30
        draw.rectangle([80, y_start, width-80, y_start + 30], fill=color)

    title_text = "FILL IN THE BLANKS"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 120), title_text, fill='white', font=title_font)

    draw.rectangle([100, header_height, width-100, header_height + 5], fill='#3498db')

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


def generate_fill_in_blank(standard_data, grade_level, output_filename="fill_in_blank.png"):
    """Generate smart TPT-style fill-in-the-blank worksheet"""

    print(f"Generating fill-in-blank worksheet for {standard_data['code']}...")

    # Get smart content engine
    content = get_smart_content()

    # Generate vocabulary
    print("   Generating vocabulary...")
    vocabulary = content.generate_vocabulary_words(standard_data['title'], count=12)

    # Create sentences with blanks
    sentences = []
    answers = []

    for word in vocabulary[:10]:
        definition = content.get_definition(word, grade_level)

        # Create fill-in-blank sentence from definition
        sentence = definition.replace(word, "___________")

        # If word isn't in definition, create a sentence
        if sentence == definition:
            if grade_level == "K-2":
                sentence = f"A ___________ is {definition.lower()}"
            elif grade_level == "3-5":
                sentence = f"The term ___________ means {definition.lower()}"
            else:
                sentence = f"A ___________ can be defined as {definition.lower()}"

        sentences.append((sentence, word))
        answers.append(word)

    print(f"   Generated {len(sentences)} fill-in-blank questions")

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
             "Directions: Fill in each blank with the correct term from the word bank.",
             fill='#2c3e50', font=text_font)

    # Word bank section
    word_bank_y = instructions_y + 110
    draw.rectangle([120, word_bank_y - 30, width-120, word_bank_y - 25], fill='#3498db')

    draw.rectangle([150, word_bank_y, width-150, word_bank_y + 70],
                   fill='#f39c12', outline='#e67e22', width=3)
    bbox = draw.textbbox((0, 0), "WORD BANK", font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, word_bank_y + 10), "WORD BANK", fill='white', font=header_font)

    # Display word bank in columns
    word_bank_content_y = word_bank_y + 90
    col_width = (width - 400) // 3

    for i, word in enumerate(answers):
        col_num = i % 3
        row_num = i // 3
        x_pos = 200 + col_num * col_width
        y_pos = word_bank_content_y + row_num * 60

        draw.rectangle([x_pos - 10, y_pos - 5, x_pos + 350, y_pos + 45],
                      fill='#ffeaa7', outline='#f39c12', width=2)
        draw.text((x_pos + 10, y_pos + 5), word.title(), fill='#2c3e50', font=text_font)

    # Sentences section
    sentences_y = word_bank_content_y + 250
    draw.rectangle([120, sentences_y - 30, width-120, sentences_y - 25], fill='#3498db')

    for i, (sentence, answer) in enumerate(sentences):
        sentence_y = sentences_y + i * 120

        # Number in circle
        draw.ellipse([140, sentence_y, 190, sentence_y + 50], fill='#f39c12')
        draw.text((155, sentence_y + 8), str(i+1), fill='white', font=text_font)

        # Sentence box
        draw.rectangle([220, sentence_y - 10, width-140, sentence_y + 90],
                      fill='#fff9e6', outline='#f39c12', width=2)

        # Wrap long sentences
        words = sentence.split()
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

        # Draw wrapped text
        for j, line in enumerate(lines[:2]):  # Max 2 lines
            draw.text((240, sentence_y + j * 45), line, fill='#2c3e50', font=small_font)

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
    print(f"Fill-in-blank worksheet saved: {output_filename}")

    # Generate answer key
    generate_answer_key(sentences, standard_data, grade_level,
                       output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_answer_key(sentences, standard_data, grade_level, output_filename):
    """Generate answer key"""
    width, height = 2550, 3300
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

    draw.rectangle([100, header_height, width-100, header_height + 5], fill='#3498db')

    info_y = header_height + 30
    draw.text((120, info_y), f"Grade: {grade_level}", fill='#2c3e50', font=subtitle_font)
    draw.text((width - 700, info_y), f"Standard: {standard_data['code']}", fill='#2c3e50', font=subtitle_font)

    # Answers section
    list_y = info_y + 100
    draw.rectangle([120, list_y - 20, width-120, list_y - 15], fill='#3498db')

    draw.rectangle([150, list_y, width-150, list_y + 70],
                   fill='#27ae60', outline='#229954', width=3)
    bbox = draw.textbbox((0, 0), "CORRECT ANSWERS", font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, list_y + 10), "CORRECT ANSWERS", fill='white', font=header_font)

    list_y += 110

    # Display answers
    for i, (sentence, answer) in enumerate(sentences):
        answer_y = list_y + i * 80

        draw.rectangle([200, answer_y - 5, width-200, answer_y + 60],
                      fill='#d4edda', outline='#27ae60', width=3)

        # Number
        draw.ellipse([220, answer_y + 5, 265, answer_y + 50], fill='#f39c12')
        draw.text((233, answer_y + 10), str(i+1), fill='white', font=text_font)

        # Answer with highlight
        draw.rectangle([300, answer_y + 5, 750, answer_y + 50],
                      fill='#ffeb3b', outline='#fbc02d', width=3)
        draw.text((320, answer_y + 10), answer.upper(), fill='#2c3e50', font=text_font)

        # Checkmark
        draw.ellipse([width - 300, answer_y + 5, width - 255, answer_y + 50],
                    fill='#27ae60', outline='#229954', width=2)
        draw.text((width - 288, answer_y + 7), "V", fill='white', font=text_font)

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

    generate_fill_in_blank(sample_standard, "6-8", "output/test_fill_in_blank.png")

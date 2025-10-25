"""
Smart Short Answer Generator
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
    colors = ['#9b59b6', '#8e44ad', '#7d3c98']  # Purple gradient

    for i, color in enumerate(colors):
        y_start = 80 + i * 30
        draw.rectangle([80, y_start, width-80, y_start + 30], fill=color)

    title_text = "SHORT ANSWER"
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


def generate_short_answer(standard_data, grade_level, output_filename="short_answer.png"):
    """Generate smart TPT-style short answer worksheet"""

    print(f"Generating short answer worksheet for {standard_data['code']}...")

    # Get smart content engine
    content = get_smart_content()

    # Generate vocabulary
    print("   Generating questions...")
    vocabulary = content.generate_vocabulary_words(standard_data['title'], count=8)

    # Create questions
    questions = []
    answers = []

    for word in vocabulary[:6]:
        definition = content.get_definition(word, grade_level)
        fun_fact = content.get_fun_fact(word)

        # Create different question types
        if grade_level == "K-2":
            question = f"What is a {word.lower()}?"
            answer = f"A {word.lower()} is {definition.lower()}"
        elif grade_level == "3-5":
            question = f"Explain what a {word.lower()} is and why it is important."
            answer = f"A {word.lower()} is {definition}. {fun_fact}"
        else:
            question = f"Define {word.lower()} and describe its role in biological systems."
            answer = f"A {word.lower()} is {definition}. {fun_fact}"

        questions.append(question)
        answers.append(answer)

    print(f"   Generated {len(questions)} short answer questions")

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
             "Directions: Answer each question with complete sentences.",
             fill='#2c3e50', font=text_font)

    # Questions section
    questions_y = instructions_y + 120
    draw.rectangle([120, questions_y - 30, width-120, questions_y - 25], fill='#e67e22')

    for i, question in enumerate(questions):
        question_y = questions_y + i * 420

        # Number in circle
        draw.ellipse([140, question_y, 200, question_y + 60], fill='#9b59b6')
        draw.text((158, question_y + 10), str(i+1), fill='white', font=header_font)

        # Question box
        draw.rectangle([220, question_y - 10, width-140, question_y + 80],
                      fill='#f3e5f5', outline='#9b59b6', width=3)

        # Wrap question text
        words = question.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=text_font)
            if bbox[2] - bbox[0] < 2100:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Draw question
        for j, line in enumerate(lines[:2]):
            draw.text((240, question_y + j * 50), line, fill='#2c3e50', font=text_font)

        # Answer lines
        answer_start_y = question_y + 110
        for line_num in range(5):
            line_y = answer_start_y + line_num * 60
            draw.line([(140, line_y), (width-140, line_y)], fill='#bdc3c7', width=2)

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
    print(f"Short answer worksheet saved: {output_filename}")

    # Generate answer key
    generate_answer_key(questions, answers, standard_data, grade_level,
                       output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_answer_key(questions, answers, standard_data, grade_level, output_filename):
    """Generate answer key"""
    width, height = 2550, 3300
    answer_key = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(answer_key)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 65)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 40)
        small_font = ImageFont.truetype("arial.ttf", 36)
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
    bbox = draw.textbbox((0, 0), "SAMPLE ANSWERS", font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, list_y + 10), "SAMPLE ANSWERS", fill='white', font=header_font)

    list_y += 110

    # Display Q&A
    for i, (question, answer) in enumerate(zip(questions, answers)):
        qa_y = list_y + i * 420

        # Question number and text
        draw.rectangle([140, qa_y - 10, width-140, qa_y + 70],
                      fill='#f3e5f5', outline='#9b59b6', width=3)

        draw.ellipse([160, qa_y, 210, qa_y + 50], fill='#9b59b6')
        draw.text((175, qa_y + 8), str(i+1), fill='white', font=text_font)

        # Question
        words = question.split()
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

        for j, line in enumerate(lines[:2]):
            draw.text((230, qa_y + j * 45), line, fill='#2c3e50', font=small_font)

        # Answer box
        answer_y = qa_y + 90
        draw.rectangle([140, answer_y, width-140, answer_y + 280],
                      fill='#d4edda', outline='#27ae60', width=3)

        # Answer text
        words = answer.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=small_font)
            if bbox[2] - bbox[0] < 2150:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        for j, line in enumerate(lines[:5]):
            draw.text((160, answer_y + 20 + j * 50), line, fill='#2c3e50', font=small_font)

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

    generate_short_answer(sample_standard, "6-8", "output/test_short_answer.png")

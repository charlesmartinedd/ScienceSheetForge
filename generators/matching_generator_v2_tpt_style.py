"""
MATCHING ACTIVITY - Teachers Pay Teachers Professional Style
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
    colors = ['#e74c3c', '#c0392b', '#a93226']  # Red gradient for matching

    for i, color in enumerate(colors):
        y_start = 80 + i * 30
        draw.rectangle([80, y_start, width-80, y_start + 30], fill=color)

    # Title - large and centered
    title_text = "MATCHING ACTIVITY"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 120), title_text, fill='white', font=title_font)

    # Decorative line under header
    draw.rectangle([100, header_height, width-100, header_height + 5], fill='#f39c12')

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


def generate_matching(standard_data, grade_level, output_filename="matching_tpt.png"):
    """Generate BEAUTIFUL TPT-style matching activity"""

    vocabulary = standard_data['vocabulary'][:10]

    # Create simple definitions
    definitions = {
        "cell": "The basic unit of life",
        "organism": "A living thing",
        "plant": "Makes its own food using sunlight",
        "animal": "Must eat other organisms for food",
        "energy": "The ability to do work or cause change",
        "matter": "Anything that has mass and takes up space",
        "ecosystem": "All living and nonliving things in an area",
        "habitat": "The natural home of an organism",
        "photosynthesis": "Process where plants make food using sunlight",
        "respiration": "Process of breaking down food to release energy",
        "nucleus": "Control center of a cell",
        "mitochondria": "Part of cell that produces energy",
        "chloroplast": "Part of plant cell where photosynthesis happens",
        "DNA": "Genetic material that carries instructions",
        "gene": "A section of DNA that codes for a trait",
        "adaptation": "A feature that helps an organism survive",
        "predator": "An animal that hunts other animals",
        "prey": "An animal that is hunted by a predator",
        "producer": "Organism that makes its own food",
        "consumer": "Organism that eats other living things",
    }

    # Select words that have definitions
    available_words = [w for w in vocabulary if w.lower() in definitions]
    if len(available_words) < 8:
        available_words = list(definitions.keys())[:10]

    selected = random.sample(available_words, min(10, len(available_words)))

    # Shuffle definitions
    shuffled_defs = [(w, definitions[w.lower()]) for w in selected]
    random.shuffle(shuffled_defs)

    # CREATE BEAUTIFUL WORKSHEET
    width, height = 2550, 3300  # 8.5x11 at 300 DPI
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

    # Add decorative border
    draw_decorative_border(draw, width, height)

    # Draw beautiful header
    content_start_y = draw_tpt_header(draw, width, standard_data, grade_level,
                                      (title_font, header_font, subtitle_font))

    # Instructions box - styled
    instructions_y = content_start_y
    draw.rectangle([120, instructions_y, width-120, instructions_y + 80],
                   fill='#fff3cd', outline='#ffc107', width=3)
    draw.text((140, instructions_y + 15),
             "Directions: Draw a line from each term to its matching definition.",
             fill='#2c3e50', font=text_font)

    # Column headers
    y_start = instructions_y + 120

    # Decorative separator
    draw.rectangle([120, y_start - 30, width-120, y_start - 25], fill='#f39c12')

    # Two columns with styled boxes
    # TERMS column
    draw.rectangle([150, y_start, 900, y_start + 70],
                   fill='#e74c3c', outline='#c0392b', width=3)
    bbox = draw.textbbox((0, 0), "TERMS", font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text((525 - text_width // 2, y_start + 10), "TERMS", fill='white', font=header_font)

    # DEFINITIONS column
    draw.rectangle([width//2 + 100, y_start, width-150, y_start + 70],
                   fill='#3498db', outline='#2980b9', width=3)
    bbox = draw.textbbox((0, 0), "DEFINITIONS", font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width//2 + 100 + width - 150) // 2 - text_width // 2, y_start + 10),
             "DEFINITIONS", fill='white', font=header_font)

    # Draw terms and definitions with styled boxes
    y_pos = y_start + 110

    for i, word in enumerate(selected):
        # Term (left side) - with styled box
        term_y = y_pos + i * 95

        # Styled term box
        draw.rectangle([170, term_y - 5, 880, term_y + 55],
                      fill='#ffe5e5', outline='#e74c3c', width=2)

        # Number in circle
        draw.ellipse([180, term_y, 220, term_y + 40], fill='#e74c3c')
        draw.text((190, term_y + 5), str(i+1), fill='white', font=text_font)

        # Term text
        draw.text((240, term_y + 5), word.title(), fill='#2c3e50', font=text_font)

        # Answer line in styled box
        draw.rectangle([700, term_y + 5, 870, term_y + 45],
                      fill='white', outline='#e74c3c', width=2)
        draw.text((780, term_y + 7), "____", fill='#bdc3c7', font=text_font)

        # Definition (right side) - shuffled, styled
        def_word, definition = shuffled_defs[i]
        def_y = y_pos + i * 95

        # Styled definition box
        draw.rectangle([width//2 + 120, def_y - 5, width-170, def_y + 55],
                      fill='#e3f2fd', outline='#3498db', width=2)

        # Letter in circle
        letter = chr(65 + i)  # A, B, C, etc.
        draw.ellipse([width//2 + 135, def_y, width//2 + 175, def_y + 40], fill='#3498db')
        draw.text((width//2 + 147, def_y + 5), letter, fill='white', font=text_font)

        # Definition text (wrap if too long)
        if len(definition) > 45:
            definition = definition[:45] + "..."
        draw.text((width//2 + 195, def_y + 5), definition, fill='#2c3e50', font=small_font)

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
    print(f"TPT-Style matching activity saved: {output_filename}")

    # Generate answer key
    generate_matching_answer_key(selected, shuffled_defs, standard_data, grade_level,
                                 output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_matching_answer_key(terms, shuffled_defs, standard_data, grade_level, output_filename):
    """Generate beautiful TPT-style answer key for matching"""

    width, height = 2550, 3300  # 8.5x11 at 300 DPI
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

    # Add decorative border
    draw_decorative_border(draw, width, height)

    # Red gradient header for answer key
    header_height = 280
    colors = ['#e74c3c', '#c0392b', '#a93226']

    for i, color in enumerate(colors):
        y_start = 80 + i * 30
        draw.rectangle([80, y_start, width-80, y_start + 30], fill=color)

    # Title - large and centered
    title_text = "ANSWER KEY"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 120), title_text, fill='white', font=title_font)

    # Decorative line under header
    draw.rectangle([100, header_height, width-100, header_height + 5], fill='#f39c12')

    # Info section
    info_y = header_height + 30
    draw.text((120, info_y), f"Grade: {grade_level}", fill='#2c3e50', font=subtitle_font)
    draw.text((width - 700, info_y), f"Standard: {standard_data['code']}",
             fill='#2c3e50', font=subtitle_font)

    # Answers section
    list_y = info_y + 100

    # Decorative separator
    draw.rectangle([120, list_y - 20, width-120, list_y - 15], fill='#f39c12')

    # Header
    draw.rectangle([150, list_y, width-150, list_y + 70],
                   fill='#27ae60', outline='#229954', width=3)
    bbox = draw.textbbox((0, 0), "CORRECT MATCHES", font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, list_y + 10), "CORRECT MATCHES", fill='white', font=header_font)

    list_y += 110

    # Display answers with styled boxes
    for i, term in enumerate(terms):
        # Find the matching definition
        for j, (def_word, definition) in enumerate(shuffled_defs):
            if term.lower() == def_word.lower():
                letter = chr(65 + j)

                # Styled answer box
                answer_y = list_y + i * 85
                draw.rectangle([200, answer_y - 5, width-200, answer_y + 60],
                              fill='#d4edda', outline='#27ae60', width=3)

                # Number in circle
                draw.ellipse([220, answer_y + 5, 265, answer_y + 50], fill='#e74c3c')
                draw.text((233, answer_y + 10), str(i+1), fill='white', font=text_font)

                # Term
                draw.text((290, answer_y + 10), f"{term.title()}", fill='#2c3e50', font=text_font)

                # Equals sign
                draw.text((width//2 - 50, answer_y + 10), "=", fill='#27ae60', font=header_font)

                # Letter in circle
                draw.ellipse([width//2 + 50, answer_y + 5, width//2 + 95, answer_y + 50], fill='#3498db')
                draw.text((width//2 + 63, answer_y + 10), letter, fill='white', font=text_font)

                # Checkmark
                draw.ellipse([width - 300, answer_y + 5, width - 255, answer_y + 50],
                            fill='#27ae60', outline='#229954', width=2)
                draw.text((width - 288, answer_y + 7), "V", fill='white', font=text_font)

                break

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
        'vocabulary': ['cell', 'nucleus', 'mitochondria', 'chloroplast', 'organism',
                      'energy', 'photosynthesis', 'respiration', 'DNA', 'adaptation']
    }

    generate_matching(sample_standard, "6-8", "output/examples/OPTION4_TPT_STYLE_matching.png")

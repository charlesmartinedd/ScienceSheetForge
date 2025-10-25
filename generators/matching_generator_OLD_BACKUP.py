"""
Matching Activity Generator
Match terms to definitions
"""

import random
from PIL import Image, ImageDraw, ImageFont


def generate_matching(standard_data, grade_level, output_filename="matching.png"):
    """Generate matching activity"""

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

    # Create worksheet - Traditional educational style
    width, height = 2550, 3300  # 8.5x11 at 300 DPI
    worksheet = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(worksheet)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 70)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 42)
        small_font = ImageFont.truetype("arial.ttf", 38)
    except:
        title_font = header_font = subtitle_font = text_font = small_font = ImageFont.load_default()

    # SIMPLE PROFESSIONAL HEADER
    draw.text((width//2 - 600, 100), "MATCHING ACTIVITY", fill='black', font=title_font)

    # Thin decorative line under title
    draw.rectangle([200, 230, width-200, 235], fill='black')

    # Grade and Standard info - simple, clean
    draw.text((150, 280), f"Grade {grade_level}", fill='black', font=subtitle_font)
    draw.text((width - 650, 280), f"{standard_data['code']}", fill='black', font=subtitle_font)

    # Topic line - simple and clean
    draw.text((150, 360), f"Topic: {standard_data['title']}", fill='black', font=header_font)

    # Name line for student
    draw.text((150, 420), "Name: ___________________________", fill='black', font=text_font)

    # Instructions - simple and clear
    draw.text((150, 500), "Directions: Draw a line from each term to its matching definition.",
             fill='black', font=text_font)

    # Column headers - Simple and clean
    y_start = 600

    # Simple dividing line
    draw.rectangle([150, y_start - 20, width-150, y_start - 17], fill='black')

    # Two columns
    draw.text((250, y_start), "TERMS", fill='black', font=header_font)
    draw.text((width//2 + 300, y_start), "DEFINITIONS", fill='black', font=header_font)

    # Draw terms and definitions
    y_pos = y_start + 100
    term_positions = []
    def_positions = []

    for i, word in enumerate(selected):
        # Term (left side) - simple with line for student to write letter
        term_y = y_pos + i * 90
        draw.text((200, term_y), f"{i+1}. {word.title()}",
                 fill='black', font=text_font)
        # Line for answer
        draw.text((550, term_y), "_____", fill='black', font=text_font)
        term_positions.append((term_y + 30, i))

        # Definition (right side) - shuffled, simple
        def_word, definition = shuffled_defs[i]
        def_y = y_pos + i * 90

        # Letter label
        letter = chr(65 + i)  # A, B, C, etc.
        draw.text((width//2 + 200, def_y), f"{letter}. {definition}",
                 fill='black', font=small_font)
        def_positions.append((def_y + 30, def_word))

    # SIMPLE FOOTER
    footer_y = height - 150

    # Simple line at bottom
    draw.rectangle([150, footer_y, width-150, footer_y + 2], fill='black')

    # Simple branding - small and unobtrusive
    draw.text((width//2 - 350, footer_y + 30),
             "ScienceSheetForge - Science Worksheets", fill='gray', font=small_font)

    worksheet.save(output_filename, quality=100, dpi=(300, 300))
    print(f"Matching activity saved: {output_filename}")

    # Generate answer key
    generate_matching_answer_key(selected, shuffled_defs, standard_data, grade_level,
                                 output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_matching_answer_key(terms, shuffled_defs, standard_data, grade_level, output_filename):
    """Generate answer key for matching - Traditional style"""

    width, height = 2550, 3300  # 8.5x11 at 300 DPI
    answer_key = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(answer_key)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 70)
        text_font = ImageFont.truetype("arial.ttf", 45)
    except:
        title_font = header_font = text_font = ImageFont.load_default()

    # SIMPLE header for answer key
    draw.text((width//2 - 450, 100), "ANSWER KEY", fill='black', font=title_font)

    # Thin decorative line
    draw.rectangle([200, 230, width-200, 235], fill='black')

    # Answers - simple and clean
    list_y = 360

    # Simple header
    draw.text((width//2 - 350, list_y), "CORRECT MATCHES:", fill='black', font=header_font)
    list_y += 120

    # Thin dividing line
    draw.rectangle([150, list_y - 30, width-150, list_y - 27], fill='black')

    for i, term in enumerate(terms):
        # Find the matching definition
        for j, (def_word, definition) in enumerate(shuffled_defs):
            if term.lower() == def_word.lower():
                letter = chr(65 + j)
                draw.text((200, list_y), f"{i+1}. {term.title()}  =  {letter}",
                         fill='black', font=text_font)
                list_y += 75
                break

    answer_key.save(output_filename, quality=100, dpi=(300, 300))
    print(f"Answer key saved: {output_filename}")

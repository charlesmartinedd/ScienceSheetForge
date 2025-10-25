"""
PROFESSIONAL Crossword Puzzle Generator
Print-ready, beautiful, engaging worksheets for Teachers Pay Teachers
"""

import random
from PIL import Image, ImageDraw, ImageFont


# COMPREHENSIVE CLUE DATABASE
SCIENCE_CLUES = {
    "cell": "The smallest unit of life that can function independently",
    "nucleus": "The control center of the cell that contains DNA",
    "mitochondria": "The powerhouse of the cell that produces energy (ATP)",
    "chloroplast": "Green organelle in plant cells where photosynthesis occurs",
    "ribosome": "Tiny structure that builds proteins in the cell",
    "membrane": "Thin barrier that surrounds and protects the cell",
    "cytoplasm": "Jelly-like substance that fills the cell",
    "vacuole": "Storage sac in cells, especially large in plant cells",
    "organism": "Any living thing, from bacteria to blue whales",
    "tissue": "Group of similar cells working together",
    "organ": "Body part made of different tissues working together",
    "system": "Group of organs that work together for a function",
    "dna": "Molecule that carries genetic instructions for life",
    "protein": "Large molecule made of amino acids that does work in cells",
    "energy": "The ability to do work or cause change",
    "atp": "Energy molecule that powers most cellular processes",
    "photosynthesis": "Process where plants make food using sunlight",
    "respiration": "Process that releases energy from food molecules",
    "glucose": "Simple sugar that is the main energy source for cells",
    "oxygen": "Gas that animals breathe in and plants produce",
    "carbon": "Element that is the backbone of all organic molecules",
    "water": "H2O - Essential molecule for all known life",
    "enzyme": "Protein that speeds up chemical reactions in cells",
    "gene": "Segment of DNA that codes for a specific trait",
    "chromosome": "Coiled structure of DNA and protein in the nucleus",
    "organelle": "Specialized structure within a cell",
    "plant": "Organism that makes its own food through photosynthesis",
    "animal": "Organism that must consume other organisms for energy",
    "bacteria": "Single-celled organism without a nucleus",
    "fungus": "Organism that absorbs nutrients from dead matter",
}


def generate_crossword(standard_data, grade_level, output_filename="crossword.png"):
    """Generate BEAUTIFUL professional crossword puzzle"""

    vocabulary = standard_data['vocabulary'][:15]
    available_words = [w for w in vocabulary if w.lower() in SCIENCE_CLUES]

    if len(available_words) < 8:
        available_words = list(SCIENCE_CLUES.keys())[:12]

    selected_words = random.sample(available_words, min(10, len(available_words)))
    selected_words.sort(key=len, reverse=True)

    # Simple placement algorithm
    grid_size = 20
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    placements = []

    # Place first word horizontally
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

    # Try to place more words
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

                            if new_row >= 0 and new_row + len(word_upper) < grid_size:
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

                            if new_col >= 0 and new_col + len(word_upper) < grid_size:
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

    # CREATE PROFESSIONAL WORKSHEET - Traditional Educational Style
    width, height = 2550, 3300  # 8.5x11 at 300 DPI
    worksheet = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(worksheet)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 70)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 45)
        small_font = ImageFont.truetype("arial.ttf", 38)
        num_font = ImageFont.truetype("arial.ttf", 32)
    except:
        title_font = header_font = subtitle_font = text_font = small_font = num_font = ImageFont.load_default()

    # SIMPLE PROFESSIONAL HEADER - Traditional worksheet style
    # Title at top
    draw.text((width//2 - 600, 100), "CROSSWORD PUZZLE", fill='black', font=title_font)

    # Thin decorative line under title
    draw.rectangle([200, 230, width-200, 235], fill='black')

    # Grade and Standard info - simple, clean
    draw.text((150, 280), f"Grade {grade_level}", fill='black', font=subtitle_font)
    draw.text((width - 700, 280), f"{standard_data['code']}", fill='black', font=subtitle_font)

    # Topic line - simple and clean
    draw.text((150, 360), f"Topic: {standard_data['title']}", fill='black', font=header_font)

    # TRADITIONAL CROSSWORD GRID - Clean and professional
    cell_size = 70  # Large enough to write in
    grid_start_x = 200
    grid_start_y = 480

    # Name line for student
    draw.text((150, 420), "Name: ___________________________", fill='black', font=text_font)

    # Draw grid - traditional black and white
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] != ' ':
                x = grid_start_x + col * cell_size
                y = grid_start_y + row * cell_size

                # Simple black borders, white cells - traditional crossword style
                draw.rectangle([x, y, x + cell_size, y + cell_size],
                             fill='white', outline='black', width=3)

    # Add numbers - traditional style (small, top-left corner)
    for placement in placements:
        x = grid_start_x + placement['col'] * cell_size
        y = grid_start_y + placement['row'] * cell_size
        draw.text((x + 4, y + 1), str(placement['number']), fill='black', font=num_font)

    # CLUES SECTION - Traditional simple layout
    clues_y = grid_start_y + (grid_size * cell_size) + 80

    # Simple dividing line
    draw.rectangle([150, clues_y - 20, width-150, clues_y - 17], fill='black')

    # ACROSS - simple bold header
    draw.text((150, clues_y), "ACROSS", fill='black', font=header_font)
    clues_y += 90

    across_clues = [p for p in placements if p['direction'] == 'across']
    for placement in across_clues[:6]:
        clue = SCIENCE_CLUES.get(placement['word'].lower(), "Science vocabulary term")
        # Wrap long clues
        if len(clue) > 52:
            clue = clue[:52] + "..."
        draw.text((180, clues_y), f"{placement['number']}. {clue}",
                 fill='black', font=text_font)
        clues_y += 65

    # DOWN - simple bold header
    down_x = width // 2 + 50
    clues_y = grid_start_y + (grid_size * cell_size) + 60

    draw.text((down_x, clues_y), "DOWN", fill='black', font=header_font)
    clues_y += 90

    down_clues = [p for p in placements if p['direction'] == 'down']
    for placement in down_clues[:6]:
        clue = SCIENCE_CLUES.get(placement['word'].lower(), "Science vocabulary term")
        if len(clue) > 48:
            clue = clue[:48] + "..."
        draw.text((down_x + 30, clues_y), f"{placement['number']}. {clue}",
                 fill='black', font=text_font)
        clues_y += 65

    # SIMPLE FOOTER - Traditional worksheet style
    footer_y = height - 150

    # Simple line at bottom
    draw.rectangle([150, footer_y, width-150, footer_y + 2], fill='black')

    # Simple branding - small and unobtrusive
    draw.text((width//2 - 350, footer_y + 30),
             "ScienceSheetForge - Science Worksheets", fill='gray', font=small_font)

    worksheet.save(output_filename, quality=100, dpi=(300, 300))
    print(f"BEAUTIFUL crossword saved: {output_filename}")

    # Generate answer key
    generate_answer_key(grid, grid_size, standard_data, placements,
                       output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_answer_key(grid, grid_size, standard_data, placements, output_filename):
    """Generate professional answer key - Traditional style"""

    width, height = 2550, 3300
    answer_key = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(answer_key)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 70)
        text_font = ImageFont.truetype("arial.ttf", 50)
        grid_font = ImageFont.truetype("arial.ttf", 42)
    except:
        title_font = header_font = text_font = grid_font = ImageFont.load_default()

    # SIMPLE header for answer key
    draw.text((width//2 - 450, 100), "ANSWER KEY", fill='black', font=title_font)

    # Thin decorative line
    draw.rectangle([200, 230, width-200, 235], fill='black')

    # Draw FILLED grid - light gray background for filled cells
    cell_size = 70
    grid_start_x = 200
    grid_start_y = 360

    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] != ' ':
                x = grid_start_x + col * cell_size
                y = grid_start_y + row * cell_size

                # Light gray background with black borders
                draw.rectangle([x, y, x + cell_size, y + cell_size],
                             fill='#f0f0f0', outline='black', width=3)

                # Draw letter BIG and CLEAR in black
                letter = grid[row][col]
                draw.text((x + 20, y + 10), letter, fill='black', font=grid_font)

    # Word list - simple and clean
    list_y = grid_start_y + (grid_size * cell_size) + 100

    # Simple header
    draw.text((width//2 - 300, list_y), "VOCABULARY WORDS", fill='black', font=header_font)
    list_y += 100

    # Thin dividing line
    draw.rectangle([150, list_y - 20, width-150, list_y - 17], fill='black')

    # Two columns
    col1_x = 250
    col2_x = width // 2 + 150

    for i, placement in enumerate(placements):
        x_pos = col1_x if i < len(placements) // 2 else col2_x
        y_pos = list_y + (i % ((len(placements) // 2) + 1)) * 75
        draw.text((x_pos, y_pos),
                 f"{placement['word'].upper()}", fill='black', font=text_font)

    answer_key.save(output_filename, quality=100, dpi=(300, 300))
    print(f"Answer key saved: {output_filename}")

"""
Word Search Generator
Creates science vocabulary word search puzzles
"""

import random
from PIL import Image, ImageDraw, ImageFont


def generate_word_search(standard_data, grade_level, output_filename="word_search.png"):
    """Generate word search puzzle"""

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

    # Create worksheet - Traditional educational style
    width, height = 2550, 3300  # 8.5x11 at 300 DPI
    worksheet = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(worksheet)

    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        header_font = ImageFont.truetype("arial.ttf", 70)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 45)
        grid_font = ImageFont.truetype("arial.ttf", 38)
        small_font = ImageFont.truetype("arial.ttf", 38)
    except:
        title_font = header_font = subtitle_font = text_font = grid_font = small_font = ImageFont.load_default()

    # SIMPLE PROFESSIONAL HEADER
    draw.text((width//2 - 450, 100), "WORD SEARCH", fill='black', font=title_font)

    # Thin decorative line under title
    draw.rectangle([200, 230, width-200, 235], fill='black')

    # Grade and Standard info - simple, clean
    draw.text((150, 280), f"Grade {grade_level}", fill='black', font=subtitle_font)
    draw.text((width - 650, 280), f"{standard_data['code']}", fill='black', font=subtitle_font)

    # Topic line - simple and clean
    draw.text((150, 360), f"Topic: {standard_data['title']}", fill='black', font=header_font)

    # Name line for student
    draw.text((150, 420), "Name: ___________________________", fill='black', font=text_font)

    # Draw grid - Traditional style with larger cells
    cell_size = 60  # Larger for easier reading and writing
    grid_start_x = 300
    grid_start_y = 520

    for row in range(grid_size):
        for col in range(grid_size):
            x = grid_start_x + col * cell_size
            y = grid_start_y + row * cell_size
            # Simple black borders, white cells
            draw.rectangle([x, y, x + cell_size, y + cell_size],
                         fill='white', outline='black', width=2)
            # Center letters in cells
            draw.text((x + 18, y + 8), grid[row][col], fill='black', font=grid_font)

    # Word list - Simple and clean
    list_y = grid_start_y + (grid_size * cell_size) + 80

    # Simple dividing line
    draw.rectangle([150, list_y - 20, width-150, list_y - 17], fill='black')

    # Simple header
    draw.text((150, list_y), "FIND THESE WORDS:", fill='black', font=header_font)
    list_y += 100

    # Display words in 3 columns
    col_width = (width - 400) // 3
    for i, word in enumerate(placed_words):
        col_num = i % 3
        row_num = i // 3
        x_pos = 200 + col_num * col_width
        y_pos = list_y + row_num * 65
        draw.text((x_pos, y_pos), f"• {word.title()}", fill='black', font=text_font)

    # SIMPLE FOOTER
    footer_y = height - 150

    # Simple line at bottom
    draw.rectangle([150, footer_y, width-150, footer_y + 2], fill='black')

    # Simple branding - small and unobtrusive
    draw.text((width//2 - 350, footer_y + 30),
             "ScienceSheetForge - Science Worksheets", fill='gray', font=small_font)

    worksheet.save(output_filename, quality=100, dpi=(300, 300))
    print(f"Word search saved: {output_filename}")

    # Generate answer key
    generate_word_search_answer_key(grid, grid_size, standard_data, placed_words, grade_level,
                                    output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_word_search_answer_key(grid, grid_size, standard_data, words, grade_level, output_filename):
    """Generate answer key - Traditional style"""

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

    # Word list - simple and clean
    list_y = 360

    # Simple header
    draw.text((width//2 - 350, list_y), "WORDS IN PUZZLE:", fill='black', font=header_font)
    list_y += 120

    # Thin dividing line
    draw.rectangle([150, list_y - 30, width-150, list_y - 27], fill='black')

    col_width = (width - 400) // 3
    for i, word in enumerate(words):
        col_num = i % 3
        row_num = i // 3
        x_pos = 200 + col_num * col_width
        y_pos = list_y + row_num * 70
        draw.text((x_pos, y_pos), f"{word.upper()}", fill='black', font=text_font)

    answer_key.save(output_filename, quality=100, dpi=(300, 300))
    print(f"Answer key saved: {output_filename}")

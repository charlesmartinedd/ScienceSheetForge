"""
Cell Hero Worksheet Generator

This example creates a fun "Super Cell Heroes" worksheet with AI-generated content.
Students learn about immune system cells through superhero characters!
"""

import sys
import os

# Add parent directory to path to import generators and config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from generators.ai_content_generator import generate_worksheet_content
from config import USE_AI_CONTENT


# Cell Hero data
CELL_HEROES = [
    {"name": "White Blood Warrior", "power": "Fights bacteria and viruses", "type": "Leukocyte"},
    {"name": "Macrophage Man", "power": "Eats invaders whole!", "type": "Macrophage"},
    {"name": "T-Cell Titan", "power": "Remembers past enemies", "type": "T-Cell"},
    {"name": "Antibody Ace", "power": "Tags bad guys for capture", "type": "B-Cell"},
    {"name": "Natural Killer", "power": "Destroys infected cells", "type": "NK Cell"},
]

SCENARIOS = [
    "A cold virus enters through your nose!",
    "Bacteria invades through a cut on your finger!",
    "Your body detects a harmful toxin!",
]


def create_fallback_avatar(hero_name):
    """
    Create a simple avatar badge when API is unavailable

    Args:
        hero_name (str): Name of the hero

    Returns:
        PIL.Image: Simple avatar badge
    """
    # Create a 200x200 image
    avatar = Image.new('RGB', (200, 200), '#ffffff')
    draw = ImageDraw.Draw(avatar)

    # Draw colorful circle background
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    color = colors[hash(hero_name) % len(colors)]
    draw.ellipse([10, 10, 190, 190], fill=color, outline='#2c3e50', width=4)

    # Draw initials
    initials = ''.join([word[0] for word in hero_name.split()[:2]])
    try:
        font = ImageFont.truetype("arial.ttf", 64)
    except:
        font = ImageFont.load_default()

    # Center the text
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (200 - text_width) // 2
    y = (200 - text_height) // 2

    draw.text((x, y), initials, fill='#ffffff', font=font)

    return avatar


def generate_character_avatar(hero_name, style="adventurer"):
    """
    Generate a unique character using DiceBear API with fallback

    Args:
        hero_name (str): Name to seed the character
        style (str): Art style (adventurer, pixel-art, lorelei, etc.)

    Returns:
        PIL.Image: Character avatar image
    """
    try:
        url = f"https://api.dicebear.com/9.x/{style}/png?seed={hero_name}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200 and len(response.content) > 100:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"API unavailable: {e}")

    print("Using fallback avatar...")
    return create_fallback_avatar(hero_name)


def create_fallback_diagram():
    """
    Create a simple flowchart diagram when API is unavailable

    Returns:
        PIL.Image: Diagram image
    """
    diagram = Image.new('RGB', (550, 350), '#ffffff')
    draw = ImageDraw.Draw(diagram)

    try:
        font = ImageFont.truetype("arial.ttf", 16)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Define boxes for the flow
    boxes = [
        {"text": "Pathogen\nEnters Body", "pos": (225, 20), "color": "#ff6b6b"},
        {"text": "White Blood Cell\nDetects", "pos": (225, 100), "color": "#4ecdc4"},
        {"text": "Sends Signal", "pos": (225, 180), "color": "#45b7d1"},
        {"text": "More Cells\nArrive", "pos": (225, 260), "color": "#f9ca24"},
    ]

    # Draw boxes and arrows
    for i, box in enumerate(boxes):
        x, y = box['pos']
        # Draw box
        draw.rectangle([x - 80, y - 25, x + 80, y + 25], fill=box['color'], outline='#2c3e50', width=2)
        # Draw text
        lines = box['text'].split('\n')
        for j, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            draw.text((x - text_width // 2, y - 10 + j * 20), line, fill='#ffffff', font=font)

        # Draw arrow to next box
        if i < len(boxes) - 1:
            draw.line([(x, y + 25), (x, y + 50)], fill='#2c3e50', width=3)
            # Arrow head
            draw.polygon([(x, y + 50), (x - 5, y + 40), (x + 5, y + 40)], fill='#2c3e50')

    # Title
    draw.text((10, 10), "Immune Response Flow", fill='#2c3e50', font=font)

    return diagram


def generate_cell_diagram():
    """
    Generate a simple immune system diagram using Kroki/Mermaid with fallback

    Returns:
        PIL.Image: Diagram image
    """
    try:
        import base64
        import zlib

        # Mermaid diagram showing immune response
        diagram = """
graph TD
    A[Pathogen Enters Body] -->|Detected| B[White Blood Cell]
    B -->|Sends Signal| C[More Immune Cells]
    C -->|Attack| D[Destroy Pathogen]
    D --> E[Body Safe!]

    style A fill:#ff6b6b
    style B fill:#4ecdc4
    style C fill:#45b7d1
    style D fill:#f9ca24
    style E fill:#6ab04c
"""

        # Encode for Kroki
        compressed = zlib.compress(diagram.encode('utf-8'))
        encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')

        # Get diagram from Kroki
        url = f"https://kroki.io/mermaid/png/{encoded}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200 and len(response.content) > 100:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"API unavailable: {e}")

    print("Using fallback diagram...")
    return create_fallback_diagram()


def create_fallback_chart():
    """
    Create a simple line chart when API is unavailable

    Returns:
        PIL.Image: Chart image
    """
    chart = Image.new('RGB', (550, 350), '#ffffff')
    draw = ImageDraw.Draw(chart)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
        small_font = ImageFont.truetype("arial.ttf", 10)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Chart area
    margin = 50
    chart_width = 450
    chart_height = 250
    left = margin
    right = left + chart_width
    top = margin
    bottom = top + chart_height

    # Draw axes
    draw.line([(left, bottom), (right, bottom)], fill='#2c3e50', width=2)  # X-axis
    draw.line([(left, bottom), (left, top)], fill='#2c3e50', width=2)  # Y-axis

    # Data points
    days = ["0", "1", "2", "3", "4", "5"]
    immune_cells = [10, 25, 50, 75, 90, 100]
    pathogens = [100, 95, 75, 40, 15, 5]

    # Calculate positions
    x_step = chart_width / (len(days) - 1)
    y_scale = chart_height / 100

    # Draw immune cells line (green)
    immune_points = []
    for i, value in enumerate(immune_cells):
        x = left + i * x_step
        y = bottom - value * y_scale
        immune_points.append((x, y))

    for i in range(len(immune_points) - 1):
        draw.line([immune_points[i], immune_points[i + 1]], fill='#4bc0c0', width=3)

    # Draw circles at points
    for x, y in immune_points:
        draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill='#4bc0c0', outline='#2c3e50')

    # Draw pathogens line (red)
    pathogen_points = []
    for i, value in enumerate(pathogens):
        x = left + i * x_step
        y = bottom - value * y_scale
        pathogen_points.append((x, y))

    for i in range(len(pathogen_points) - 1):
        draw.line([pathogen_points[i], pathogen_points[i + 1]], fill='#ff6384', width=3)

    # Draw circles at points
    for x, y in pathogen_points:
        draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill='#ff6384', outline='#2c3e50')

    # Draw X-axis labels
    for i, day in enumerate(days):
        x = left + i * x_step
        draw.text((x - 10, bottom + 10), f"Day {day}", fill='#2c3e50', font=small_font)

    # Draw Y-axis labels
    for i in range(0, 101, 25):
        y = bottom - i * y_scale
        draw.text((left - 40, y - 8), str(i), fill='#2c3e50', font=small_font)

    # Title
    draw.text((left + chart_width // 2 - 80, 10), "Immune Response Over Time", fill='#2c3e50', font=font)

    # Legend
    draw.rectangle([right - 140, top + 10, right - 130, top + 20], fill='#4bc0c0')
    draw.text((right - 125, top + 10), "Immune Cells", fill='#2c3e50', font=small_font)

    draw.rectangle([right - 140, top + 30, right - 130, top + 40], fill='#ff6384')
    draw.text((right - 125, top + 30), "Pathogens", fill='#2c3e50', font=small_font)

    return chart


def generate_immune_response_chart():
    """
    Generate a chart showing immune response over time using QuickChart with fallback

    Returns:
        PIL.Image: Chart image
    """
    try:
        chart_config = {
            "type": "line",
            "data": {
                "labels": ["Day 0", "Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
                "datasets": [
                    {
                        "label": "Immune Cells",
                        "data": [10, 25, 50, 75, 90, 100],
                        "borderColor": "rgb(75, 192, 192)",
                        "fill": False
                    },
                    {
                        "label": "Pathogens",
                        "data": [100, 95, 75, 40, 15, 5],
                        "borderColor": "rgb(255, 99, 132)",
                        "fill": False
                    }
                ]
            },
            "options": {
                "title": {
                    "display": True,
                    "text": "Immune Response Over Time"
                }
            }
        }

        import json
        from urllib.parse import quote

        config_str = json.dumps(chart_config)
        url = f"https://quickchart.io/chart?c={quote(config_str)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200 and len(response.content) > 100:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"API unavailable: {e}")

    print("Using fallback chart...")
    return create_fallback_chart()


def create_cell_hero_worksheet(output_filename="cell_hero_worksheet.png", grade_level="3-5", use_ai=None):
    """
    Create a complete Cell Hero worksheet with AI-generated content

    Args:
        output_filename (str): Output file name
        grade_level (str): K-2, 3-5, or 6-8
        use_ai (bool): Whether to use AI content generation (None = use config default)
    """
    # Determine whether to use AI
    if use_ai is None:
        use_ai = USE_AI_CONTENT

    # Generate content (AI or fallback)
    content = generate_worksheet_content(grade_level=grade_level, use_ai=use_ai)
    hero = content['hero']
    scenario = content['scenario']
    questions = content['questions']

    # Create worksheet canvas (8.5x11 inches at 150 DPI)
    width, height = 1275, 1650
    worksheet = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(worksheet)

    # Try to use a standard font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        header_font = ImageFont.truetype("arial.ttf", 32)
        text_font = ImageFont.truetype("arial.ttf", 24)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Title
    title = "🦸 SUPER CELL HEROES 🦸"
    draw.text((100, 50), title, fill='#2c3e50', font=title_font)

    # Subtitle
    subtitle = "Learn about your body's amazing defenders!"
    draw.text((100, 120), subtitle, fill='#7f8c8d', font=text_font)

    y_offset = 180

    # Generate and add character avatar
    print("Generating Cell Hero character...")
    character = generate_character_avatar(hero['name'])

    if character:
        # Resize character to fit
        character = character.resize((200, 200))
        worksheet.paste(character, (100, y_offset), character if character.mode == 'RGBA' else None)

    # Hero information
    draw.text((320, y_offset), f"Meet: {hero['name']}", fill='#e74c3c', font=header_font)
    draw.text((320, y_offset + 50), f"Type: {hero['type']}", fill='#3498db', font=text_font)
    draw.text((320, y_offset + 90), f"Power: {hero['power']}", fill='#2ecc71', font=text_font)

    y_offset += 250

    # Scenario
    draw.text((100, y_offset), "🚨 EMERGENCY SCENARIO:", fill='#e74c3c', font=header_font)
    draw.text((100, y_offset + 50), scenario, fill='#34495e', font=text_font)

    y_offset += 120

    # Questions section
    draw.text((100, y_offset), "📝 MISSION QUESTIONS:", fill='#9b59b6', font=header_font)

    y_offset += 50
    for question in questions:
        draw.text((100, y_offset), question, fill='#2c3e50', font=text_font)
        y_offset += 40
        # Add answer line
        draw.line([(120, y_offset), (1150, y_offset)], fill='#bdc3c7', width=2)
        y_offset += 50

    # Add diagram
    print("Generating immune response diagram...")
    diagram = generate_cell_diagram()
    if diagram:
        # Resize to fit
        diagram.thumbnail((550, 300))
        worksheet.paste(diagram, (100, y_offset))

    # Add chart
    print("Generating immune response chart...")
    chart = generate_immune_response_chart()
    if chart:
        # Resize to fit
        chart.thumbnail((550, 300))
        worksheet.paste(chart, (680, y_offset))

    # Footer
    draw.text((100, height - 80), "🧬 Science is Super! 🔬", fill='#95a5a6', font=text_font)

    # Save worksheet
    worksheet.save(output_filename)
    print(f"✅ Worksheet saved as {output_filename}")
    print(f"   Hero: {hero['name']}")
    print(f"   Scenario: {scenario}")


if __name__ == "__main__":
    print("🔬 Cell Hero Worksheet Generator 🔬")
    print("=" * 50)

    # Show AI status
    if USE_AI_CONTENT:
        print("🤖 AI Content Generation: ENABLED")
    else:
        print("📋 AI Content Generation: DISABLED (using templates)")
    print()

    # Generate a single worksheet
    create_cell_hero_worksheet()

    print("\n🎉 Done! Check your worksheet!")
    print("\nTo generate multiple variations, run:")
    print("  for i in range(10):")
    print("      create_cell_hero_worksheet(f'worksheet_{i}.png')")
    print("\nTo use different grade levels:")
    print("  create_cell_hero_worksheet('k2_worksheet.png', grade_level='K-2')")
    print("  create_cell_hero_worksheet('middle_worksheet.png', grade_level='6-8')")

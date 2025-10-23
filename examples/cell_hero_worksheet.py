"""
Cell Hero Worksheet Generator

This example creates a fun "Super Cell Heroes" worksheet using free APIs.
Students learn about immune system cells through superhero characters!
"""

import requests
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


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


def generate_character_avatar(hero_name, style="adventurer"):
    """
    Generate a unique character using DiceBear API

    Args:
        hero_name (str): Name to seed the character
        style (str): Art style (adventurer, pixel-art, lorelei, etc.)

    Returns:
        PIL.Image: Character avatar image
    """
    url = f"https://api.dicebear.com/9.x/{style}/png?seed={hero_name}"

    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Error generating character: {response.status_code}")
        return None


def generate_cell_diagram():
    """
    Generate a simple immune system diagram using Kroki/Mermaid

    Returns:
        PIL.Image: Diagram image
    """
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

    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Error generating diagram: {response.status_code}")
        return None


def generate_immune_response_chart():
    """
    Generate a chart showing immune response over time using QuickChart

    Returns:
        PIL.Image: Chart image
    """
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

    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Error generating chart: {response.status_code}")
        return None


def create_cell_hero_worksheet(output_filename="cell_hero_worksheet.png"):
    """
    Create a complete Cell Hero worksheet

    Args:
        output_filename (str): Output file name
    """
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
    hero = random.choice(CELL_HEROES)
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
    scenario = random.choice(SCENARIOS)
    draw.text((100, y_offset + 50), scenario, fill='#34495e', font=text_font)

    y_offset += 120

    # Questions section
    draw.text((100, y_offset), "📝 MISSION QUESTIONS:", fill='#9b59b6', font=header_font)

    questions = [
        f"1. How would {hero['name']} respond to this threat?",
        "2. What other immune cells might help?",
        "3. How long would it take to defeat the invader?",
    ]

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

    # Generate a single worksheet
    create_cell_hero_worksheet()

    print("\n🎉 Done! Check your worksheet!")
    print("\nTo generate multiple variations, run:")
    print("  for i in range(10):")
    print("      create_cell_hero_worksheet(f'worksheet_{i}.png')")

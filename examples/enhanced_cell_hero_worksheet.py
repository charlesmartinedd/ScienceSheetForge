"""
Enhanced Cell Hero Worksheet Generator

Creates professional, engaging worksheets for K-8 students with:
- Beautiful layouts and color schemes
- Interactive activities
- Answer keys
- Grade-appropriate content
"""

import requests
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
from urllib.parse import quote


# Cell Hero data with more detailed information
CELL_HEROES = [
    {
        "name": "White Blood Warrior",
        "power": "Fights bacteria and viruses",
        "type": "Leukocyte",
        "description": "Patrols your body looking for invaders!",
        "fun_fact": "Your body makes millions of white blood cells every day!",
        "color": "#FF6B6B"
    },
    {
        "name": "Macrophage Man",
        "power": "Eats invaders whole!",
        "type": "Macrophage",
        "description": "The ultimate cleanup crew!",
        "fun_fact": "Macrophage means 'big eater' in Greek!",
        "color": "#4ECDC4"
    },
    {
        "name": "T-Cell Titan",
        "power": "Remembers past enemies",
        "type": "T-Cell",
        "description": "Never forgets a villain!",
        "fun_fact": "T-Cells can remember germs for your whole life!",
        "color": "#45B7D1"
    },
    {
        "name": "Antibody Ace",
        "power": "Tags bad guys for capture",
        "type": "B-Cell",
        "description": "Creates special markers for invaders!",
        "fun_fact": "Your body can make billions of different antibodies!",
        "color": "#F9CA24"
    },
    {
        "name": "Natural Killer",
        "power": "Destroys infected cells",
        "type": "NK Cell",
        "description": "Protects you from infected cells!",
        "fun_fact": "NK cells work 24/7 to keep you healthy!",
        "color": "#6AB04C"
    },
]

SCENARIOS = [
    {
        "title": "Cold Virus Attack!",
        "description": "A sneaky cold virus enters through your nose!",
        "challenge": "How will your immune system respond?",
        "solution": "T-Cells and antibodies team up to remember and fight the virus!"
    },
    {
        "title": "Cut Finger Invasion!",
        "description": "Bacteria invades through a cut on your finger!",
        "challenge": "What immune cells rush to the scene first?",
        "solution": "White blood cells and macrophages arrive to eat the bacteria!"
    },
    {
        "title": "Toxin Alert!",
        "description": "Your body detects a harmful toxin!",
        "challenge": "How does your body neutralize the threat?",
        "solution": "B-Cells create antibodies to tag and remove the toxin!"
    },
]


def generate_character_avatar(hero_name, style="adventurer"):
    """Generate a unique character using DiceBear API"""
    url = f"https://api.dicebear.com/9.x/{style}/png?seed={hero_name}&size=300"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error generating character: {e}")
    return None


def generate_immune_response_chart():
    """Generate an improved chart showing immune response over time"""
    chart_config = {
        "type": "line",
        "data": {
            "labels": ["Day 0", "Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
            "datasets": [
                {
                    "label": "Immune Cells",
                    "data": [10, 25, 50, 75, 90, 100],
                    "borderColor": "rgb(75, 192, 192)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "fill": True,
                    "borderWidth": 3
                },
                {
                    "label": "Pathogens",
                    "data": [100, 95, 75, 40, 15, 5],
                    "borderColor": "rgb(255, 99, 132)",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "fill": True,
                    "borderWidth": 3
                }
            ]
        },
        "options": {
            "title": {
                "display": True,
                "text": "Immune Response Over Time",
                "fontSize": 20,
                "fontColor": "#2c3e50"
            },
            "legend": {
                "display": True,
                "position": "bottom"
            },
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": True,
                        "max": 100
                    },
                    "scaleLabel": {
                        "display": True,
                        "labelString": "Cell Count"
                    }
                }]
            }
        }
    }

    try:
        config_str = json.dumps(chart_config)
        url = f"https://quickchart.io/chart?width=600&height=350&c={quote(config_str)}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error generating chart: {e}")
    return None


def draw_rounded_rectangle(draw, coords, radius, fill, outline=None, width=1):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = coords
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline, width=width)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline, width=width)
    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill, outline=outline)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill, outline=outline)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill, outline=outline)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill, outline=outline)


def draw_text_with_outline(draw, pos, text, font, fill, outline_color='white', outline_width=2):
    """Draw text with an outline for better visibility"""
    x, y = pos
    # Draw outline
    for adj_x in range(-outline_width, outline_width + 1):
        for adj_y in range(-outline_width, outline_width + 1):
            draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)
    # Draw main text
    draw.text(pos, text, font=font, fill=fill)


def create_enhanced_cell_hero_worksheet(grade_level="K-5", output_filename="enhanced_cell_hero_worksheet.png"):
    """
    Create an enhanced, professional Cell Hero worksheet

    Args:
        grade_level (str): Target grade level (K-2, 3-5, 6-8)
        output_filename (str): Output file name
    """
    # Create worksheet canvas (8.5x11 inches at 200 DPI for better quality)
    width, height = 1700, 2200
    worksheet = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(worksheet)

    # Load fonts with better fallback handling
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        header_font = ImageFont.truetype("arial.ttf", 40)
        subheader_font = ImageFont.truetype("arial.ttf", 32)
        text_font = ImageFont.truetype("arial.ttf", 28)
        small_font = ImageFont.truetype("arial.ttf", 22)
    except:
        try:
            title_font = ImageFont.truetype("Arial.ttf", 60)
            header_font = ImageFont.truetype("Arial.ttf", 40)
            subheader_font = ImageFont.truetype("Arial.ttf", 32)
            text_font = ImageFont.truetype("Arial.ttf", 28)
            small_font = ImageFont.truetype("Arial.ttf", 22)
        except:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            subheader_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

    # Draw colorful header background
    draw_rounded_rectangle(draw, [50, 30, width-50, 180], 20, fill='#3498db')

    # Title with shadow effect
    title = "SUPER CELL HEROES"
    draw_text_with_outline(draw, (150, 60), title, title_font, fill='#ffffff', outline_color='#2c3e50', outline_width=3)

    # Subtitle
    subtitle = "Learn about your body's amazing defenders!"
    draw.text((150, 125), subtitle, fill='#ecf0f1', font=subheader_font)

    y_offset = 220

    # Random hero selection
    hero = random.choice(CELL_HEROES)
    scenario = random.choice(SCENARIOS)

    # Hero Card Section with colored background
    draw_rounded_rectangle(draw, [80, y_offset, width-80, y_offset+320], 15, fill='#ecf0f1')
    draw_rounded_rectangle(draw, [80, y_offset, width-80, y_offset+60], 15, fill=hero['color'])

    draw.text((110, y_offset + 15), "MEET YOUR HERO", fill='#ffffff', font=header_font)

    # Generate and add character avatar
    print("Generating Cell Hero character...")
    character = generate_character_avatar(hero['name'])

    if character:
        character = character.resize((250, 250))
        # Add circular mask
        mask = Image.new('L', (250, 250), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, 250, 250], fill=255)

        # Create a white background circle
        draw.ellipse([110, y_offset+70, 360, y_offset+320], fill='white')
        worksheet.paste(character, (110, y_offset+70), mask)

    # Hero information with colored boxes
    info_x = 400
    info_y = y_offset + 80

    draw.text((info_x, info_y), f"Name: {hero['name']}", fill='#e74c3c', font=header_font)
    draw.text((info_x, info_y + 50), f"Type: {hero['type']}", fill='#3498db', font=text_font)
    draw.text((info_x, info_y + 90), f"Power: {hero['power']}", fill='#2ecc71', font=text_font)
    draw.text((info_x, info_y + 130), f"{hero['description']}", fill='#7f8c8d', font=small_font)

    # Fun Fact box
    draw_rounded_rectangle(draw, [info_x, info_y+170, width-120, info_y+230], 10, fill='#fff9e6', outline='#f9ca24', width=2)
    draw.text((info_x + 15, info_y + 180), f"Fun Fact: {hero['fun_fact']}", fill='#2c3e50', font=small_font)

    y_offset += 360

    # Scenario Section
    draw_rounded_rectangle(draw, [80, y_offset, width-80, y_offset+220], 15, fill='#ffe6e6')
    draw_rounded_rectangle(draw, [80, y_offset, width-80, y_offset+60], 15, fill='#e74c3c')
    draw.text((110, y_offset + 15), "EMERGENCY SCENARIO", fill='#ffffff', font=header_font)

    draw.text((110, y_offset + 80), scenario['title'], fill='#c0392b', font=subheader_font)
    draw.text((110, y_offset + 125), scenario['description'], fill='#2c3e50', font=text_font)
    draw.text((110, y_offset + 170), f"Challenge: {scenario['challenge']}", fill='#e74c3c', font=text_font)

    y_offset += 250

    # Questions Section
    draw_rounded_rectangle(draw, [80, y_offset, width-80, y_offset+450], 15, fill='#f0e6ff')
    draw_rounded_rectangle(draw, [80, y_offset, width-80, y_offset+60], 15, fill='#9b59b6')
    draw.text((110, y_offset + 15), "MISSION QUESTIONS", fill='#ffffff', font=header_font)

    questions = [
        f"1. How would {hero['name']} respond to this threat?",
        "2. What other immune cells might help in this situation?",
        "3. How many days would it take to defeat the invader?",
        "4. Draw what you think the battle looks like!"
    ]

    y_offset += 80
    for i, question in enumerate(questions):
        draw.text((110, y_offset), question, fill='#2c3e50', font=text_font)
        y_offset += 45

        if i < 3:  # Add lines for written answers
            for line in range(2):
                y_offset += 5
                draw.line([(130, y_offset), (width-110, y_offset)], fill='#bdc3c7', width=2)
                y_offset += 30
        else:  # Drawing box for question 4
            draw_rounded_rectangle(draw, [130, y_offset+5, width-110, y_offset+120], 10, fill='white', outline='#9b59b6', width=2)
            y_offset += 125

    y_offset += 20

    # Chart Section
    print("Generating immune response chart...")
    chart = generate_immune_response_chart()
    if chart:
        chart.thumbnail((width-200, 400))
        chart_y = y_offset
        worksheet.paste(chart, (100, chart_y))
        y_offset = chart_y + chart.height + 30

    # Footer with grade level and branding
    footer_y = height - 100
    draw_rounded_rectangle(draw, [80, footer_y, width-80, footer_y+60], 10, fill='#2c3e50')
    draw.text((width//2 - 200, footer_y + 15), "Science is Super!", fill='#ecf0f1', font=subheader_font)
    draw.text((110, footer_y + 35), f"Grade Level: {grade_level}", fill='#95a5a6', font=small_font)
    draw.text((width - 400, footer_y + 35), "ScienceSheetForge", fill='#95a5a6', font=small_font)

    # Save worksheet
    worksheet.save(output_filename, quality=95, optimize=True)
    print(f"\nWorksheet saved as {output_filename}")
    print(f"Hero: {hero['name']}")
    print(f"Scenario: {scenario['title']}")
    print(f"Grade Level: {grade_level}")

    # Generate answer key
    generate_answer_key(hero, scenario, output_filename.replace('.png', '_ANSWER_KEY.png'))

    return worksheet


def generate_answer_key(hero, scenario, output_filename="answer_key.png"):
    """Generate a professional answer key"""
    width, height = 1700, 2200
    answer_key = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(answer_key)

    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        header_font = ImageFont.truetype("arial.ttf", 40)
        text_font = ImageFont.truetype("arial.ttf", 28)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = header_font = text_font = small_font = ImageFont.load_default()

    # Header
    draw_rounded_rectangle(draw, [50, 30, width-50, 180], 20, fill='#27ae60')
    draw_text_with_outline(draw, (250, 60), "ANSWER KEY", title_font, fill='#ffffff', outline_color='#1e8449', outline_width=3)
    draw.text((400, 125), "For Teachers Only", fill='#ecf0f1', font=text_font)

    y = 230

    # Answers section
    draw.text((100, y), "SAMPLE ANSWERS:", fill='#27ae60', font=header_font)
    y += 60

    answers = [
        f"1. {hero['name']} would use their power to {hero['power'].lower()}. They would {hero['description'].lower()}",
        "2. Other immune cells that might help: White blood cells, Macrophages, T-Cells, B-Cells, and Natural Killer cells.",
        "3. It typically takes 3-5 days for the immune system to fully respond and defeat the invader.",
        "4. Students' drawings should show immune cells surrounding and attacking the pathogen."
    ]

    for answer in answers:
        # Wrap text if too long
        words = answer.split()
        line = ""
        for word in words:
            if len(line + word) < 85:
                line += word + " "
            else:
                draw.text((100, y), line, fill='#2c3e50', font=text_font)
                y += 40
                line = "   " + word + " "
        if line:
            draw.text((100, y), line, fill='#2c3e50', font=text_font)
        y += 60

    # Learning objectives
    y += 40
    draw.text((100, y), "LEARNING OBJECTIVES:", fill='#27ae60', font=header_font)
    y += 60

    objectives = [
        "- Understand the role of immune cells in defending the body",
        "- Identify different types of immune cells and their functions",
        "- Explain the timeline of immune response",
        "- Visualize biological processes through creative drawing"
    ]

    for obj in objectives:
        draw.text((120, y), obj, fill='#2c3e50', font=text_font)
        y += 50

    # Additional teaching tips
    y += 40
    draw_rounded_rectangle(draw, [80, y, width-80, y+300], 15, fill='#e8f8f5')
    draw.text((100, y+20), "TEACHING TIPS:", fill='#16a085', font=header_font)
    y += 80

    tips = [
        "• Use the character to make immune cells relatable and memorable",
        "• Discuss real-life scenarios where students got sick and recovered",
        "• Have students create their own immune cell superheroes",
        "• Connect to current events about vaccines and immunity",
        "• Use the chart to teach data interpretation skills"
    ]

    for tip in tips:
        draw.text((120, y), tip, fill='#2c3e50', font=small_font)
        y += 45

    answer_key.save(output_filename, quality=95, optimize=True)
    print(f"Answer key saved as {output_filename}")


if __name__ == "__main__":
    print("=" * 60)
    print("ENHANCED CELL HERO WORKSHEET GENERATOR")
    print("=" * 60)
    print("\nCreating professional, engaging worksheets for K-8 students!")
    print("-" * 60)

    # Generate worksheets for different grade levels
    create_enhanced_cell_hero_worksheet(grade_level="K-5", output_filename="K5_cell_hero_worksheet.png")

    print("\n" + "=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    print("\nGenerated files:")
    print("1. K5_cell_hero_worksheet.png - Student worksheet")
    print("2. K5_cell_hero_worksheet_ANSWER_KEY.png - Teacher answer key")
    print("\nWorksheets are ready for printing or digital use!")

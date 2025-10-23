# 🚀 Getting Started with ScienceSheetForge

## Quick Start Guide

### 1. Install Python
Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Your First Worksheet Generator
```bash
cd examples
python cell_hero_worksheet.py
```

This will create a `cell_hero_worksheet.png` file with a randomly generated superhero cell character!

---

## 📚 What Can You Create?

### Example Worksheets Included:
- **cell_hero_worksheet.py** - Superhero immune cells with adventures

### Coming Soon:
- Disease Detective mysteries
- Feedback Loop roller coasters
- Build-a-Creature design sheets
- Cell Olympics competitions

---

## 🎨 Customization Tips

### Change Character Styles
In `cell_hero_worksheet.py`, change the style parameter:
```python
character = generate_character_avatar(hero['name'], style="pixel-art")
```

Available styles:
- `adventurer` - Adventure characters
- `pixel-art` - Retro 8-bit style
- `lorelei` - Cartoon people
- `fun-emoji` - Emoji-style faces
- `bottts` - Robot characters
- `avataaars` - Avatar-style characters

### Adjust Worksheet Size
Change the DPI or dimensions:
```python
# For higher quality (300 DPI)
width, height = 2550, 3300  # 8.5x11 at 300 DPI

# For smaller file size (72 DPI)
width, height = 612, 792    # 8.5x11 at 72 DPI
```

### Add Your Branding
Edit the footer section to add your Teachers Pay Teachers shop name:
```python
draw.text((100, height - 80), "Created by YOUR SHOP NAME", fill='#95a5a6', font=text_font)
```

---

## 🔄 Batch Generation

Create 20 different worksheets at once:

```python
for i in range(20):
    create_cell_hero_worksheet(f"worksheet_{i:02d}.png")
```

This creates:
- worksheet_00.png
- worksheet_01.png
- worksheet_02.png
- ... through worksheet_19.png

Each with different:
- Cell hero characters
- Emergency scenarios
- Random variations

---

## 📤 Export to PDF

To convert PNG worksheets to PDF for Teachers Pay Teachers:

```python
from PIL import Image

# Single image to PDF
img = Image.open("cell_hero_worksheet.png")
img.save("cell_hero_worksheet.pdf", "PDF")

# Multiple images to one PDF
images = [Image.open(f"worksheet_{i:02d}.png") for i in range(5)]
images[0].save("worksheet_bundle.pdf", save_all=True, append_images=images[1:])
```

---

## 🎯 Next Steps

1. **Explore the APIs** - Check out the free APIs in the README
2. **Create your own content** - Add to the `content/` directory
3. **Design templates** - Build reusable layouts
4. **Integrate with Canva** - Use Canva API for professional polish

---

## 💡 Pro Tips for Teachers Pay Teachers

### File Preparation
- Export at 300 DPI for print quality
- Include answer keys
- Create preview images (show first page)
- Bundle related worksheets together

### Pricing Strategy
- Individual worksheets: $1-3
- Worksheet bundles (5-10): $5-10
- Complete units (20+): $15-25

### SEO Keywords
Include in your product description:
- Cell biology worksheets
- Science activities K-8
- Immune system lesson
- STEM education
- Hands-on learning
- Distance learning resources

---

## 🆘 Troubleshooting

### "Module not found" error
```bash
pip install requests Pillow
```

### Font errors on Windows
The script will automatically fall back to default fonts if Arial isn't found.

To use custom fonts:
```python
font = ImageFont.truetype("path/to/your/font.ttf", 48)
```

### API timeout errors
Some free APIs have rate limits. Add a small delay between requests:
```python
import time
time.sleep(1)  # Wait 1 second between API calls
```

---

## 📞 Need Help?

- Check the [main README](README.md) for full documentation
- Open an [issue on GitHub](https://github.com/YOUR_USERNAME/ScienceSheetForge/issues)
- Join the discussions for tips and tricks

---

**Happy Creating! 🧬🔬**

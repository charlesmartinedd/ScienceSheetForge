# 🔬 ScienceSheetForge - AI-Powered Science Worksheet Generator

**Create stunning, TPT-ready science worksheets in seconds!**

[![Status](https://img.shields.io/badge/status-active%20development-brightgreen)](https://github.com/charlesmartinedd/ScienceSheetForge)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

---

## 🎯 What is ScienceSheetForge?

ScienceSheetForge is an intelligent worksheet generator that creates **professional, print-ready science worksheets** for K-8 educators. Built with a smart content engine, it generates unique, engaging, and educationally sound worksheets every time.

### ✨ Key Features

- 🤖 **Smart Content Engine** - Rich vocabulary database with 50+ science terms
- 📚 **Multiple Worksheet Types** - Crosswords, word searches, matching, and more
- 🎨 **Professional Design** - TPT-quality layouts at 300 DPI
- 📊 **NGSS Aligned** - Integrated with Next Generation Science Standards
- 🎓 **Grade-Level Adaptive** - Content appropriate for K-2, 3-5, and 6-8
- ⚡ **Instant Generation** - Create worksheets in under 3 seconds
- 💰 **100% Free** - No API costs, works completely offline

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A TrueType font such as Arial or DejaVu Sans available to Pillow for consistent print quality output

### Installation

```bash
# Clone the repository
git clone https://github.com/charlesmartinedd/ScienceSheetForge.git
cd ScienceSheetForge

# Install dependencies
pip install -r requirements.txt

# Start the web server
python app.py
```

### Usage

1. Open your browser to `http://localhost:3000`
2. Select grade level (K-2, 3-5, or 6-8)
3. Choose an NGSS standard
4. Pick a worksheet format
5. Click "Generate Worksheet"
6. Download your worksheet + answer key!

---

## 📚 Worksheet Types

### ✅ Currently Available:

1. **Crossword Puzzles** (SMART - Upgraded!) 🧩
   - AI-generated clues based on topic
   - Grade-appropriate definitions
   - Professional TPT-style layout
   - Auto-generated answer keys

2. **Word Search** 🔍
   - Topic-based vocabulary
   - Clean grid design
   - Checkbox word lists

3. **Matching Activities** 🔗
   - Term-to-definition matching
   - Styled boxes and clear layout
   - Comprehensive answer keys

### 🔜 Coming Soon:

4. Fill-in-the-Blank
5. Short Answer Questions
6. True/False Quizzes
7. Multiple Choice Tests
8. Vocabulary Cards
9. Diagram Labeling
10. And 10+ more creative formats!

---

## 🎨 What Makes Our Worksheets "Stunning"?

### Professional Design
- ✅ 300 DPI output for perfect printing
- ✅ Decorative borders and headers
- ✅ Color-coded sections
- ✅ Professional typography
- ✅ Consistent branding

### Educational Quality
- ✅ NGSS-aligned content
- ✅ Grade-appropriate language
- ✅ Multiple definition styles (standard, kid-friendly, fun facts)
- ✅ Real-world examples
- ✅ Scientifically accurate

### Unique Every Time
- ✅ Smart vocabulary selection
- ✅ Varied question types
- ✅ Different layouts
- ✅ Engaging scenarios
- ✅ No two worksheets are exactly alike

---

## 🧬 Smart Content Engine

Our proprietary Smart Content Engine provides:

### Comprehensive Vocabulary Database
- **50+ science terms** with rich descriptions
- **4 definition types** per term:
  - Standard (scientific definition)
  - Kid-Friendly (simplified for younger students)
  - Fun Fact (interesting trivia)
  - Real-World Example (practical application)

### Coverage Areas:
- 🧪 **Cell Biology** - cells, organelles, functions
- 🔬 **Molecular Biology** - DNA, proteins, enzymes
- ⚡ **Energy & Processes** - photosynthesis, respiration, ATP
- 🌍 **Ecology** - ecosystems, habitats, food chains
- ⚛️ **Chemistry** - atoms, molecules, matter

### Example:

**Word:** mitochondria

- **Standard:** "The powerhouse organelle that produces energy (ATP)"
- **Kid-Friendly:** "The tiny power plant inside cells that makes energy"
- **Fun Fact:** "Mitochondria have their own DNA separate from the nucleus!"
- **Example:** "Mitochondria are like tiny batteries that keep cells running."

---

## 📁 Project Structure

```
ScienceSheetForge/
├── ai_engine/              # Smart Content System ⭐ NEW
│   ├── smart_content.py    # Main content engine (50+ terms)
│   ├── content_generator.py # AI integration (optional)
│   ├── question_generator.py # Question templates
│   ├── definition_generator.py # Definition management
│   └── scenario_generator.py # Story scenarios
│
├── generators/             # Worksheet Generators
│   ├── crossword_smart.py  # Smart crossword ⭐ NEW
│   ├── word_search_generator.py # Word search
│   ├── matching_generator.py # Matching activity
│   └── [more generators...]
│
├── templates/              # Web Interface
│   └── index.html          # Beautiful modal UI
│
├── app.py                  # Flask web server
├── ngss_standards.py       # NGSS standards database
├── worksheet_formats.py    # Format definitions
├── requirements.txt        # Python dependencies
└── output/                 # Generated worksheets
```

---

## 🔧 Technical Stack

**Backend:**
- Python 3.8+
- Flask (web framework)
- Pillow/PIL (image generation at 300 DPI)
- Custom Smart Content Engine

**Frontend:**
- HTML5 + CSS3 (modern design)
- Vanilla JavaScript (no dependencies)
- Modal-based workflow

**Content:**
- Smart Content Engine (template-based)
- No AI API dependency (works offline!)
- Rich educational templates

---

## 📊 Current Status

### ✅ Completed:
- [x] Smart Content Engine with 50+ terms
- [x] Smart Crossword Generator
- [x] Web Interface (modal-based, 3-step)
- [x] NGSS Standards Integration
- [x] Multiple Grade Levels (K-8)
- [x] Professional TPT-style design
- [x] Auto-generated answer keys
- [x] 300 DPI print quality

### 🔄 In Progress:
- [ ] Upgrade word search with smart content
- [ ] Upgrade matching with smart content
- [ ] Expand vocabulary to 100+ terms

### 📋 Planned:
- [ ] Fill-in-the-blank worksheets
- [ ] Short answer questions
- [ ] True/false quizzes
- [ ] Multiple choice tests
- [ ] PDF export (critical for TPT!)
- [ ] Batch generation (create 50+ worksheets at once)
- [ ] Visual enhancements (clipart, icons)
- [ ] Spanish language support

**See [COMPLETION_PLAN.md](COMPLETION_PLAN.md) for detailed roadmap**

---

## 🎓 Educational Use

### Perfect For:
- 👨‍🏫 **Teachers** - Create classroom materials quickly
- 🏫 **Homeschool Parents** - Engaging science lessons
- 📚 **Tutors** - Customized practice worksheets
- 💼 **TPT Sellers** - Create products to sell
- 🎒 **Students** - Additional practice and review

### Aligned With:
- Next Generation Science Standards (NGSS)
- Common Core State Standards
- State-specific science standards

---

## 💡 Why ScienceSheetForge?

### VS. Other Worksheet Generators:

| Feature | ScienceSheetForge | Others |
|---------|-------------------|--------|
| **AI-Powered Content** | ✅ Yes | ❌ No |
| **TPT-Quality Design** | ✅ Yes | ⚠️ Basic |
| **Print Quality** | ✅ 300 DPI | ⚠️ 72-150 DPI |
| **Cost** | ✅ Free | 💰 $5-50/mo |
| **Offline** | ✅ Works offline | ❌ Requires internet |
| **Customization** | ✅ Extensive | ⚠️ Limited |
| **Unique Content** | ✅ Every time | ❌ Repetitive |

---

## 🤝 Contributing

We welcome contributions! See [COMPLETION_PLAN.md](COMPLETION_PLAN.md) for areas that need development.

### How to Contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 Documentation

- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Current status and achievements
- **[COMPLETION_PLAN.md](COMPLETION_PLAN.md)** - Roadmap to TPT-ready product
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed setup guide

---

## 🐛 Known Issues

- PDF export not yet implemented (coming soon!)
- Some worksheet types still use basic content (being upgraded)
- Clipart integration planned but not yet added

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NGSS Standards** - Next Generation Science Standards
- **Teachers Pay Teachers** - Inspiration for quality requirements
- **Open Source Community** - Pillow, Flask, and other amazing tools
- **Educators Everywhere** - For inspiring us to build better tools

---

## 📞 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/charlesmartinedd/ScienceSheetForge/issues)
- **Discussions:** [GitHub Discussions](https://github.com/charlesmartinedd/ScienceSheetForge/discussions)
- **Email:** charlesmartinedd@github.com

---

## 🎯 Roadmap

### Phase 1 (Current): Foundation ✅
- Smart content engine
- Basic worksheet types
- Web interface

### Phase 2 (Next): Content Expansion
- Upgrade all generators
- 100+ vocabulary terms
- More worksheet types

### Phase 3: TPT-Ready Features
- PDF export
- Batch generation
- Visual enhancements
- Professional polish

### Phase 4: Launch
- TPT marketplace
- Marketing materials
- User documentation
- Video tutorials

**Estimated completion: 15-20 hours of development**

---

## ⭐ Star Us!

If you find ScienceSheetForge useful, please give us a star on GitHub! It helps others discover the project.

---

**Made with ❤️ for educators who inspire the next generation of scientists!**

🧬 **Happy Teaching!** 🔬

---

*Last Updated: October 25, 2025*
*Version: 2.0 (Smart Content Engine)*

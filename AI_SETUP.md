# AI Content Generation Setup Guide

ScienceSheetForge supports AI-powered content generation using OpenAI's GPT models. This creates unique, educational content for every worksheet!

## 🚀 Quick Start

### 1. Get an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy your API key (starts with `sk-`)

### 2. Configure Your Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file and add your API key
# You can use nano, vim, or any text editor
nano .env
```

Add your API key to `.env`:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4o-mini
USE_AI_CONTENT=true
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate AI-Powered Worksheets!

```bash
python examples/cell_hero_worksheet.py
```

## 🎛️ Configuration Options

### Model Selection

Choose different OpenAI models in your `.env` file:

```bash
# Most cost-effective (recommended for development)
OPENAI_MODEL=gpt-4o-mini

# More creative/accurate (higher cost)
OPENAI_MODEL=gpt-4o

# Legacy models (not recommended)
OPENAI_MODEL=gpt-3.5-turbo
```

### Grade Levels

Generate worksheets for different grade levels:

```python
# K-2 (ages 5-8)
create_cell_hero_worksheet('k2_worksheet.png', grade_level='K-2')

# 3-5 (ages 8-11) - Default
create_cell_hero_worksheet('elementary.png', grade_level='3-5')

# 6-8 (ages 11-14)
create_cell_hero_worksheet('middle.png', grade_level='6-8')
```

### Disable AI (Use Templates)

To use hardcoded content instead of AI:

```bash
# In .env file
USE_AI_CONTENT=false
```

Or in code:
```python
create_cell_hero_worksheet('template.png', use_ai=False)
```

## 💰 Cost Estimates

OpenAI pricing (as of 2024):

| Model | Input | Output | Cost per Worksheet* |
|-------|--------|--------|---------------------|
| gpt-4o-mini | $0.150/1M tokens | $0.600/1M tokens | ~$0.001-0.002 |
| gpt-4o | $5.00/1M tokens | $15.00/1M tokens | ~$0.02-0.05 |

*Approximate - actual cost varies based on content complexity

**Example:** Generating 100 worksheets with gpt-4o-mini costs approximately **$0.10-0.20**

## 🎨 What AI Generates

### Cell Heroes
Unique superhero characters based on real immune cells:
- Creative names (e.g., "Antibody Ace", "Neutrophil Knight")
- Accurate cell types (T-Cell, B-Cell, Macrophage, etc.)
- Kid-friendly power descriptions

### Scenarios
Engaging emergency situations:
- Age-appropriate challenges
- Scientifically plausible
- Varied contexts (virus, bacteria, toxin, injury)

### Questions
Educational questions tailored to grade level:
- Comprehension checks
- Critical thinking prompts
- Application exercises

## 🔧 Troubleshooting

### "OpenAI API key not provided"
- Make sure `.env` file exists in project root
- Verify `OPENAI_API_KEY` is set correctly
- Check for typos or extra spaces

### "Rate limit exceeded"
- You've hit OpenAI's rate limit
- Wait a minute and try again
- Consider upgrading your OpenAI plan

### "Insufficient quota"
- Add credits to your OpenAI account
- Check your [usage dashboard](https://platform.openai.com/usage)

### AI generation fails but worksheet still creates
- This is normal! The system falls back to template content
- Check your internet connection
- Verify your API key is valid

## 🔒 Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore` by default
2. **Use environment variables** in production
3. **Rotate API keys** regularly
4. **Set usage limits** in OpenAI dashboard
5. **Monitor usage** to avoid unexpected charges

## 📊 Batch Generation

Generate multiple unique worksheets:

```python
from examples.cell_hero_worksheet import create_cell_hero_worksheet

# Generate 50 unique worksheets for grades 3-5
for i in range(50):
    create_cell_hero_worksheet(
        f'output/worksheet_{i:03d}.png',
        grade_level='3-5',
        use_ai=True
    )
```

## 🆘 Getting Help

- Check [OpenAI Status](https://status.openai.com/)
- Read [OpenAI Documentation](https://platform.openai.com/docs)
- File an issue on GitHub
- Review the example code in `generators/ai_content_generator.py`

## 🎓 Next Steps

- Customize prompts in `generators/ai_content_generator.py`
- Experiment with different models
- Adjust temperature for more/less creativity
- Add your own content types (diagrams, activities, etc.)

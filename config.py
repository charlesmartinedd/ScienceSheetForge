"""
Configuration settings for ScienceSheetForge
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')  # Default to cost-effective model
USE_AI_CONTENT = os.getenv('USE_AI_CONTENT', 'true').lower() == 'true'

# Worksheet Configuration
DEFAULT_GRADE_LEVEL = os.getenv('DEFAULT_GRADE_LEVEL', '3-5')  # K-2, 3-5, or 6-8
WORKSHEET_DPI = int(os.getenv('WORKSHEET_DPI', '150'))
WORKSHEET_SIZE = (1275, 1650)  # 8.5x11 inches at 150 DPI

# Validate configuration
if USE_AI_CONTENT and not OPENAI_API_KEY:
    print("⚠️  Warning: USE_AI_CONTENT is enabled but OPENAI_API_KEY is not set!")
    print("   Create a .env file with your OpenAI API key or set USE_AI_CONTENT=false")
    print("   Example: cp .env.example .env")

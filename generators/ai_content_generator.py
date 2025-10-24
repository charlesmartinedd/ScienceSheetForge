"""
AI Content Generator using OpenAI

Generates unique, educational content for science worksheets
"""
import json
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL


class AIContentGenerator:
    """Generates worksheet content using OpenAI"""

    def __init__(self, api_key=None, model=None):
        """
        Initialize the AI content generator

        Args:
            api_key (str): OpenAI API key (defaults to config)
            model (str): Model to use (defaults to config)
        """
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or OPENAI_MODEL
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

        if not self.client:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY in .env file")

    def generate_cell_hero(self, grade_level="3-5"):
        """
        Generate a unique cell hero character

        Args:
            grade_level (str): K-2, 3-5, or 6-8

        Returns:
            dict: Hero with name, type, and power
        """
        prompt = f"""Create a fun, educational superhero character based on an immune system cell.

Grade level: {grade_level}

Return a JSON object with:
- name: Creative superhero name (e.g., "Antibody Ace", "T-Cell Titan")
- type: Actual cell type (e.g., "B-Cell", "T-Cell", "Macrophage", "NK Cell", "Neutrophil")
- power: Fun description of what this cell does (1 sentence, kid-friendly)

Make it engaging and scientifically accurate for the grade level."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an educational content creator specializing in K-8 science education."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=1.0
            )

            content = response.choices[0].message.content
            hero = json.loads(content)
            return hero

        except Exception as e:
            print(f"AI generation failed: {e}")
            # Fallback to hardcoded content
            return {
                "name": "White Blood Warrior",
                "type": "Leukocyte",
                "power": "Fights bacteria and viruses"
            }

    def generate_scenario(self, grade_level="3-5"):
        """
        Generate an emergency scenario for the worksheet

        Args:
            grade_level (str): K-2, 3-5, or 6-8

        Returns:
            str: Scenario description
        """
        prompt = f"""Create a fun, educational emergency scenario for a science worksheet about the immune system.

Grade level: {grade_level}

The scenario should:
- Be 1-2 sentences
- Describe a pathogen entering the body
- Be age-appropriate and not scary
- Be scientifically plausible
- Be engaging for students

Just return the scenario text, no JSON."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an educational content creator specializing in K-8 science education."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.0
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"AI generation failed: {e}")
            return "A cold virus enters through your nose!"

    def generate_questions(self, hero_name, scenario, grade_level="3-5", num_questions=3):
        """
        Generate educational questions based on the hero and scenario

        Args:
            hero_name (str): Name of the cell hero
            scenario (str): The emergency scenario
            grade_level (str): K-2, 3-5, or 6-8
            num_questions (int): Number of questions to generate

        Returns:
            list: List of questions
        """
        prompt = f"""Create {num_questions} educational questions for a science worksheet.

Grade level: {grade_level}
Hero: {hero_name}
Scenario: {scenario}

Requirements:
- Questions should be age-appropriate for {grade_level}
- Mix of comprehension, application, and critical thinking
- Related to immune system and the scenario
- Engaging and thought-provoking

Return a JSON array of question strings, numbered 1, 2, 3, etc."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an educational content creator specializing in K-8 science education."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.8
            )

            content = response.choices[0].message.content
            result = json.loads(content)

            # Handle different possible JSON structures
            if isinstance(result, dict):
                questions = result.get('questions', [])
            else:
                questions = result

            return questions if questions else [
                f"1. How would {hero_name} respond to this threat?",
                "2. What other immune cells might help?",
                "3. How long would it take to defeat the invader?"
            ]

        except Exception as e:
            print(f"AI generation failed: {e}")
            return [
                f"1. How would {hero_name} respond to this threat?",
                "2. What other immune cells might help?",
                "3. How long would it take to defeat the invader?"
            ]

    def generate_complete_worksheet_content(self, grade_level="3-5"):
        """
        Generate all content for a complete worksheet

        Args:
            grade_level (str): K-2, 3-5, or 6-8

        Returns:
            dict: Complete worksheet content with hero, scenario, and questions
        """
        print(f"🤖 Generating AI content for grade level {grade_level}...")

        hero = self.generate_cell_hero(grade_level)
        print(f"   ✓ Generated hero: {hero['name']}")

        scenario = self.generate_scenario(grade_level)
        print(f"   ✓ Generated scenario")

        questions = self.generate_questions(hero['name'], scenario, grade_level)
        print(f"   ✓ Generated {len(questions)} questions")

        return {
            "hero": hero,
            "scenario": scenario,
            "questions": questions,
            "grade_level": grade_level
        }


# Convenience function for backwards compatibility
def generate_worksheet_content(grade_level="3-5", use_ai=True):
    """
    Generate worksheet content (AI or fallback)

    Args:
        grade_level (str): K-2, 3-5, or 6-8
        use_ai (bool): Whether to use AI generation

    Returns:
        dict: Worksheet content
    """
    if use_ai:
        try:
            generator = AIContentGenerator()
            return generator.generate_complete_worksheet_content(grade_level)
        except Exception as e:
            print(f"⚠️  AI generation not available: {e}")
            print("   Falling back to hardcoded content...")
            use_ai = False

    # Fallback content
    import random

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

    hero = random.choice(CELL_HEROES)
    scenario = random.choice(SCENARIOS)
    questions = [
        f"1. How would {hero['name']} respond to this threat?",
        "2. What other immune cells might help?",
        "3. How long would it take to defeat the invader?",
    ]

    return {
        "hero": hero,
        "scenario": scenario,
        "questions": questions,
        "grade_level": grade_level
    }

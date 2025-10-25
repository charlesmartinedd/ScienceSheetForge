"""
Scenario Generator - Creates engaging stories and scenarios
Makes worksheets fun and relatable for students
"""

import random
from typing import List, Dict
from .content_generator import get_ai_generator


class ScenarioGenerator:
    """Generate educational scenarios and stories using AI"""

    def __init__(self):
        self.ai = get_ai_generator()

        # Story themes
        self.themes = [
            "superhero",
            "mystery",
            "adventure",
            "detective",
            "space_explorer",
            "scientist",
            "inventor",
            "nature_guide"
        ]

    def generate_story_scenario(self, topic: str, grade_level: str, theme: str = None) -> str:
        """
        Generate an engaging story scenario

        Args:
            topic: Science topic
            grade_level: Grade level (K-2, 3-5, 6-8)
            theme: Story theme (optional)

        Returns:
            Story scenario text
        """
        if theme is None:
            theme = random.choice(self.themes)

        theme_prompts = {
            "superhero": "a superhero who uses science",
            "mystery": "a mystery that needs science to solve",
            "adventure": "an adventure involving science",
            "detective": "a science detective solving a case",
            "space_explorer": "a space explorer discovering",
            "scientist": "a scientist making a discovery",
            "inventor": "an inventor creating something new",
            "nature_guide": "a nature guide teaching about"
        }

        theme_desc = theme_prompts.get(theme, "a character learning about science")

        prompt = f"""Create a fun, engaging story scenario about {topic} for grade {grade_level} students featuring {theme_desc}.

Make it:
- 3-4 sentences long
- Exciting and age-appropriate
- Educational but entertaining
- Relatable to students

Scenario:"""

        scenario = self.ai.generate_text(prompt, max_length=150, temperature=0.8)

        if not scenario or len(scenario) < 20:
            return f"Imagine you are learning about {topic}! What exciting discoveries will you make?"

        return scenario

    def generate_real_world_connection(self, topic: str, grade_level: str) -> str:
        """
        Generate a real-world connection to the topic

        Args:
            topic: Science topic
            grade_level: Grade level

        Returns:
            Real-world connection text
        """
        prompt = f"""Explain how {topic} connects to students' daily lives (grade {grade_level}).

Make it:
- Relatable and practical
- 2-3 sentences
- Shows why the topic matters

Connection:"""

        connection = self.ai.generate_text(prompt, max_length=120, temperature=0.7)

        if not connection or len(connection) < 20:
            return f"Understanding {topic} helps us make sense of the world around us!"

        return connection

    def generate_problem_scenario(self, topic: str, grade_level: str) -> Dict:
        """
        Generate a problem-solving scenario

        Args:
            topic: Science topic
            grade_level: Grade level

        Returns:
            Dictionary with problem, hints, and solution
        """
        prompt = f"""Create a problem-solving scenario about {topic} for grade {grade_level}.

Format:
Problem: [describe the problem]
Hints: [2-3 hints to help solve it]
Solution: [the answer]

Make it challenging but age-appropriate."""

        result = self.ai.generate_text(prompt, max_length=200, temperature=0.7)

        return {
            "content": result if result else "Solve this science challenge!",
            "topic": topic,
            "grade_level": grade_level,
            "type": "problem_solving"
        }

    def generate_experiment_scenario(self, topic: str, grade_level: str) -> Dict:
        """
        Generate a hands-on experiment scenario

        Args:
            topic: Science topic
            grade_level: Grade level

        Returns:
            Experiment scenario with materials and steps
        """
        prompt = f"""Create a simple, safe experiment scenario about {topic} for grade {grade_level}.

Format:
Title: [experiment name]
Materials: [what you need]
Steps: [3-4 simple steps]
What to observe: [what students should notice]

Make it safe and doable at home or school."""

        result = self.ai.generate_text(prompt, max_length=220, temperature=0.7)

        return {
            "content": result if result else "Try this science experiment!",
            "topic": topic,
            "grade_level": grade_level,
            "type": "experiment"
        }

    def generate_character_dialogue(self, topic: str, grade_level: str,
                                   character_type: str = "scientist") -> str:
        """
        Generate dialogue from a character

        Args:
            topic: Science topic
            grade_level: Grade level
            character_type: Type of character

        Returns:
            Character dialogue text
        """
        prompt = f"""Create dialogue where a friendly {character_type} explains {topic} to grade {grade_level} students.

Make it:
- Conversational and friendly
- 2-3 sentences
- Educational but not boring

Dialogue:"""

        dialogue = self.ai.generate_text(prompt, max_length=120, temperature=0.8)

        if not dialogue or len(dialogue) < 20:
            return f"Hi there! Let me tell you something amazing about {topic}..."

        return dialogue

    def generate_mission_briefing(self, topic: str, grade_level: str) -> str:
        """
        Generate a 'mission briefing' style scenario

        Args:
            topic: Science topic
            grade_level: Grade level

        Returns:
            Mission briefing text
        """
        prompt = f"""Create an exciting mission briefing about {topic} for grade {grade_level} students.

Format like a special assignment:
"MISSION: [mission name]
OBJECTIVE: [what students need to do]
IMPORTANCE: [why it matters]"

Make it exciting and motivating."""

        briefing = self.ai.generate_text(prompt, max_length=150, temperature=0.8)

        if not briefing or len(briefing) < 30:
            return f"MISSION: Master {topic}!\nOBJECTIVE: Complete this worksheet and become an expert!"

        return briefing

    def generate_choose_adventure(self, topic: str, grade_level: str) -> Dict:
        """
        Generate a choose-your-own-adventure scenario

        Args:
            topic: Science topic
            grade_level: Grade level

        Returns:
            Adventure scenario with choices
        """
        prompt = f"""Create a choose-your-own-adventure scenario about {topic} for grade {grade_level}.

Format:
Situation: [describe the situation]
Choice A: [option 1]
Choice B: [option 2]
Which leads to: [brief outcomes]

Make it fun and educational."""

        result = self.ai.generate_text(prompt, max_length=180, temperature=0.8)

        return {
            "content": result if result else "Choose your science adventure!",
            "topic": topic,
            "grade_level": grade_level,
            "type": "choose_adventure"
        }

    def generate_fun_intro(self, topic: str, grade_level: str) -> str:
        """
        Generate a fun, engaging introduction

        Args:
            topic: Science topic
            grade_level: Grade level

        Returns:
            Introduction text
        """
        prompt = f"""Write a fun, engaging introduction to {topic} for grade {grade_level} students.

Make it:
- Exciting and attention-grabbing
- 2 sentences
- Makes students want to learn more

Introduction:"""

        intro = self.ai.generate_text(prompt, max_length=100, temperature=0.8)

        if not intro or len(intro) < 20:
            return f"Get ready to explore the amazing world of {topic}!"

        return intro

"""
Question Generator - Creates engaging educational questions
Uses AI to generate age-appropriate questions
"""

import random
from typing import List, Dict
from .content_generator import get_ai_generator


class QuestionGenerator:
    """Generate educational questions using AI"""

    def __init__(self):
        self.ai = get_ai_generator()

        # Question templates for different types
        self.question_types = [
            "multiple_choice",
            "true_false",
            "fill_in_blank",
            "short_answer",
            "matching",
            "diagram_label"
        ]

    def generate_multiple_choice(self, topic: str, grade_level: str, count: int = 5) -> List[Dict]:
        """
        Generate multiple choice questions

        Args:
            topic: Science topic
            grade_level: Grade level (K-2, 3-5, 6-8)
            count: Number of questions

        Returns:
            List of question dictionaries with options and correct answer
        """
        questions = []

        for i in range(count):
            prompt = f"""Create a multiple choice question about {topic} for grade {grade_level} students.

Format:
Question: [your question]
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Correct: [letter]

Make it educational and engaging."""

            result = self.ai.generate_text(prompt, max_length=200, temperature=0.7)

            if result:
                questions.append({
                    "question": result,
                    "type": "multiple_choice",
                    "grade_level": grade_level
                })

        return questions

    def generate_true_false(self, topic: str, grade_level: str, count: int = 10) -> List[Dict]:
        """Generate true/false questions"""
        questions = []

        for i in range(count):
            prompt = f"""Create a true or false statement about {topic} for grade {grade_level}.

Format:
Statement: [your statement]
Answer: [True or False]

Make it scientifically accurate and educational."""

            result = self.ai.generate_text(prompt, max_length=100, temperature=0.6)

            if result:
                questions.append({
                    "statement": result,
                    "type": "true_false",
                    "grade_level": grade_level
                })

        return questions

    def generate_fill_in_blank(self, topic: str, grade_level: str, vocabulary: List[str]) -> List[Dict]:
        """
        Generate fill-in-the-blank questions using vocabulary

        Args:
            topic: Science topic
            grade_level: Grade level
            vocabulary: List of vocabulary words to use

        Returns:
            List of fill-in-the-blank questions
        """
        questions = []

        for word in vocabulary[:10]:
            prompt = f"""Create a fill-in-the-blank sentence about {topic} for grade {grade_level} that uses the word '{word}'.

Format:
Sentence: The _____ is [rest of sentence].
Answer: {word}

Make it educational and clear."""

            result = self.ai.generate_text(prompt, max_length=80, temperature=0.6)

            if result:
                questions.append({
                    "sentence": result,
                    "answer": word,
                    "type": "fill_in_blank",
                    "grade_level": grade_level
                })

        return questions

    def generate_short_answer(self, topic: str, grade_level: str, count: int = 5) -> List[Dict]:
        """Generate short answer questions"""
        questions = []

        question_starters = [
            "Explain how",
            "Describe what happens when",
            "Why does",
            "What would happen if",
            "Compare and contrast"
        ]

        for starter in random.sample(question_starters, min(count, len(question_starters))):
            prompt = f"""Create a short answer question about {topic} for grade {grade_level} starting with "{starter}".

Format:
Question: {starter} [complete the question]
Sample Answer: [brief correct answer]

Make it thought-provoking but age-appropriate."""

            result = self.ai.generate_text(prompt, max_length=150, temperature=0.7)

            if result:
                questions.append({
                    "question": result,
                    "type": "short_answer",
                    "grade_level": grade_level
                })

        return questions

    def generate_application_questions(self, topic: str, grade_level: str, count: int = 3) -> List[Dict]:
        """Generate real-world application questions"""
        questions = []

        for i in range(count):
            prompt = f"""Create a real-world application question about {topic} for grade {grade_level}.

Format:
Scenario: [real-world situation]
Question: [how does science apply]
Answer: [brief explanation]

Make it relatable to students' daily lives."""

            result = self.ai.generate_text(prompt, max_length=180, temperature=0.8)

            if result:
                questions.append({
                    "content": result,
                    "type": "application",
                    "grade_level": grade_level
                })

        return questions

    def generate_questions_for_worksheet(self, topic: str, standard_code: str,
                                        grade_level: str, worksheet_type: str) -> List[Dict]:
        """
        Generate appropriate questions for a specific worksheet type

        Args:
            topic: Science topic
            standard_code: NGSS standard code
            grade_level: Grade level
            worksheet_type: Type of worksheet

        Returns:
            List of questions tailored to the worksheet type
        """
        if worksheet_type in ["crossword", "word_search", "matching"]:
            # These need vocabulary-based questions
            return self.generate_vocabulary_questions(topic, grade_level)
        elif worksheet_type == "fill_in_blank":
            vocabulary = self.ai.generate_vocabulary_list(topic, standard_code, 10)
            return self.generate_fill_in_blank(topic, grade_level, vocabulary)
        elif worksheet_type == "short_answer":
            return self.generate_short_answer(topic, grade_level, 5)
        elif worksheet_type == "multiple_choice":
            return self.generate_multiple_choice(topic, grade_level, 5)
        else:
            # Default to mixed questions
            return self.generate_mixed_questions(topic, grade_level)

    def generate_vocabulary_questions(self, topic: str, grade_level: str) -> List[Dict]:
        """Generate vocabulary-focused questions"""
        questions = []

        prompt = f"""Generate 5 vocabulary questions about {topic} for grade {grade_level}.

Format each as:
Q: [question]
A: [answer]

Make them educational and fun."""

        result = self.ai.generate_text(prompt, max_length=250, temperature=0.7)

        if result:
            questions.append({
                "content": result,
                "type": "vocabulary",
                "grade_level": grade_level
            })

        return questions

    def generate_mixed_questions(self, topic: str, grade_level: str) -> List[Dict]:
        """Generate a mix of different question types"""
        questions = []

        # Get a variety
        questions.extend(self.generate_multiple_choice(topic, grade_level, 2))
        questions.extend(self.generate_short_answer(topic, grade_level, 2))
        questions.extend(self.generate_true_false(topic, grade_level, 3))

        return questions

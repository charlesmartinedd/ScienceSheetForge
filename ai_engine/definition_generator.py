"""
Definition Generator - Creates age-appropriate definitions
Adapts complexity based on grade level
"""

from typing import Dict, List
from .content_generator import get_ai_generator


class DefinitionGenerator:
    """Generate educational definitions using AI"""

    def __init__(self):
        self.ai = get_ai_generator()

    def generate_definition(self, word: str, grade_level: str, context: str = "") -> str:
        """
        Generate a single definition

        Args:
            word: Vocabulary word
            grade_level: Grade level (K-2, 3-5, 6-8)
            context: Optional context for the definition

        Returns:
            Definition string
        """
        return self.ai.generate_definition(word, grade_level)

    def generate_definitions_batch(self, words: List[str], grade_level: str) -> Dict[str, str]:
        """
        Generate definitions for multiple words

        Args:
            words: List of vocabulary words
            grade_level: Grade level

        Returns:
            Dictionary mapping words to definitions
        """
        return self.ai.batch_generate(words, grade_level, "definition")

    def generate_example_sentence(self, word: str, grade_level: str) -> str:
        """
        Generate an example sentence using the word

        Args:
            word: Vocabulary word
            grade_level: Grade level

        Returns:
            Example sentence
        """
        prompt = f"""Create one example sentence using the word '{word}' that is appropriate for grade {grade_level} students.

Make it:
- Clear and educational
- Shows the meaning of the word
- Age-appropriate

Sentence:"""

        sentence = self.ai.generate_text(prompt, max_length=60, temperature=0.6)

        if not sentence or len(sentence) < 10:
            return f"Scientists study {word} in their research."

        return sentence

    def generate_word_breakdown(self, word: str, grade_level: str) -> Dict[str, str]:
        """
        Generate a complete breakdown of a word

        Args:
            word: Vocabulary word
            grade_level: Grade level

        Returns:
            Dictionary with definition, example, and related words
        """
        definition = self.generate_definition(word, grade_level)
        example = self.generate_example_sentence(word, grade_level)

        # Generate related words
        prompt = f"""List 3 words related to '{word}' for grade {grade_level} science.

Format: word1, word2, word3"""

        related = self.ai.generate_text(prompt, max_length=40, temperature=0.5)
        related_words = [w.strip() for w in related.split(',')] if related else []

        return {
            "word": word,
            "definition": definition,
            "example": example,
            "related_words": related_words,
            "grade_level": grade_level
        }

    def generate_vocabulary_card(self, word: str, grade_level: str, topic: str) -> Dict:
        """
        Generate a complete vocabulary card with all information

        Args:
            word: Vocabulary word
            grade_level: Grade level
            topic: Science topic

        Returns:
            Complete vocabulary card data
        """
        card = {
            "word": word,
            "grade_level": grade_level,
            "topic": topic
        }

        # Definition
        card["definition"] = self.generate_definition(word, grade_level)

        # Example sentence
        card["example"] = self.generate_example_sentence(word, grade_level)

        # Fun fact
        prompt = f"""Share one interesting fact about '{word}' for grade {grade_level} students.

Make it:
- Surprising or fascinating
- Age-appropriate
- Scientifically accurate

Fact:"""

        fun_fact = self.ai.generate_text(prompt, max_length=80, temperature=0.7)
        card["fun_fact"] = fun_fact if fun_fact else f"{word.title()} is an important concept in science!"

        return card

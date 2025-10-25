"""
AI Content Generator - Core Engine
Uses Hugging Face API for intelligent content generation
"""

import requests
import json
import time
from typing import List, Dict, Optional


class AIContentGenerator:
    """Main AI content generation engine using Hugging Face"""

    def __init__(self, api_key: str = None):
        # Get API key from environment variable or parameter
        import os
        if api_key is None:
            api_key = os.environ.get('HUGGINGFACE_API_KEY', '')
        self.api_key = api_key
        self.base_url = "https://api-inference.huggingface.co/models/"

        # Models we'll use (all FREE) - Updated for 2025 API
        self.models = {
            "text_generation": "meta-llama/Llama-3.2-1B-Instruct",  # Free, fast model
            "chat": "HuggingFaceH4/zephyr-7b-beta",  # Free chat model
            "fallback": "google/flan-t5-base",  # Always available fallback
        }

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_text(self, prompt: str, max_length: int = 200, temperature: float = 0.7) -> str:
        """
        Generate text using Hugging Face inference API

        Args:
            prompt: The input prompt
            max_length: Maximum length of generated text
            temperature: Creativity level (0.0-1.0)

        Returns:
            Generated text string
        """
        # Try multiple models in order of preference
        models_to_try = [
            self.models['text_generation'],
            self.models['chat'],
            self.models['fallback']
        ]

        for model_name in models_to_try:
            url = f"{self.base_url}{model_name}"

            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_length,
                    "temperature": temperature,
                    "top_p": 0.9,
                    "do_sample": True,
                    "return_full_text": False
                }
            }

            try:
                response = requests.post(url, headers=self.headers, json=payload, timeout=30)

                # Handle rate limiting
                if response.status_code == 503:
                    time.sleep(5)
                    response = requests.post(url, headers=self.headers, json=payload, timeout=30)

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        generated = result[0].get('generated_text', '').strip()
                        if generated:
                            return generated
                    elif isinstance(result, dict):
                        generated = result.get('generated_text', '').strip()
                        if generated:
                            return generated
                elif response.status_code == 404:
                    # Model not found, try next one
                    continue
                else:
                    print(f"API Error for {model_name}: {response.status_code}")
                    continue

            except Exception as e:
                print(f"Error with {model_name}: {e}")
                continue

        # If all models fail, return empty string
        print("All models failed, using fallback content")
        return ""

    def generate_grade_appropriate_content(self, topic: str, grade_level: str, content_type: str) -> str:
        """
        Generate grade-appropriate educational content

        Args:
            topic: The educational topic
            grade_level: Grade level (K-2, 3-5, 6-8)
            content_type: Type of content (definition, question, scenario, etc.)

        Returns:
            Generated educational content
        """
        # Adjust complexity based on grade level
        complexity = {
            "K-2": "very simple, using basic vocabulary suitable for 5-7 year olds",
            "3-5": "moderately simple, using intermediate vocabulary for 8-10 year olds",
            "6-8": "moderately complex, using advanced vocabulary for 11-13 year olds"
        }

        level_desc = complexity.get(grade_level, complexity["3-5"])

        prompt = f"""You are an expert elementary science teacher. Create {content_type} about {topic} for grade {grade_level}.

Requirements:
- Make it {level_desc}
- Make it engaging and fun for students
- Keep it scientifically accurate
- Use clear, concise language

{content_type.title()}:"""

        return self.generate_text(prompt, max_length=150, temperature=0.7)

    def generate_vocabulary_list(self, topic: str, standard_code: str, count: int = 15) -> List[str]:
        """
        Generate a vocabulary list for a science topic

        Args:
            topic: Science topic
            standard_code: NGSS standard code
            count: Number of vocabulary words to generate

        Returns:
            List of vocabulary words
        """
        prompt = f"""List {count} important science vocabulary words for the topic: {topic} (NGSS {standard_code}).

Format: Just list the words, separated by commas.
Words:"""

        result = self.generate_text(prompt, max_length=100, temperature=0.5)

        if result:
            # Extract words from the response
            words = [w.strip().lower() for w in result.replace('\n', ',').split(',')]
            words = [w for w in words if w and len(w) > 2 and w.isalpha()]
            return words[:count]

        # Fallback to basic words if generation fails
        return ["cell", "organism", "energy", "matter", "plant", "animal",
                "ecosystem", "habitat", "adaptation", "photosynthesis"]

    def generate_definition(self, word: str, grade_level: str) -> str:
        """
        Generate a grade-appropriate definition for a vocabulary word

        Args:
            word: The vocabulary word
            grade_level: Grade level (K-2, 3-5, 6-8)

        Returns:
            Definition string
        """
        prompt = f"""Define '{word}' for {grade_level} students in one clear sentence.

Make it:
- Simple and easy to understand
- Scientifically accurate
- Age-appropriate for {grade_level}

Definition:"""

        definition = self.generate_text(prompt, max_length=80, temperature=0.5)

        if not definition or len(definition) < 10:
            # Fallback definitions
            fallbacks = {
                "cell": "The smallest unit of life",
                "organism": "A living thing",
                "energy": "The ability to do work or cause change",
                "matter": "Anything that has mass and takes up space",
                "ecosystem": "All living and nonliving things in an area"
            }
            return fallbacks.get(word.lower(), f"A science term related to {word}")

        return definition

    def generate_clue(self, word: str, grade_level: str, difficulty: str = "medium") -> str:
        """
        Generate a puzzle clue for a vocabulary word

        Args:
            word: The vocabulary word
            grade_level: Grade level
            difficulty: easy, medium, or hard

        Returns:
            Clue string
        """
        difficulty_desc = {
            "easy": "very obvious and direct",
            "medium": "moderately challenging",
            "hard": "challenging but fair"
        }

        prompt = f"""Create a {difficulty_desc[difficulty]} crossword puzzle clue for the word '{word}' suitable for {grade_level} students.

Make it:
- Fun and engaging
- Age-appropriate
- {difficulty_desc[difficulty]}

Clue:"""

        clue = self.generate_text(prompt, max_length=60, temperature=0.6)

        if not clue or len(clue) < 5:
            return self.generate_definition(word, grade_level)

        return clue

    def batch_generate(self, words: List[str], grade_level: str, content_type: str = "definition") -> Dict[str, str]:
        """
        Generate content for multiple words in batch

        Args:
            words: List of vocabulary words
            grade_level: Grade level
            content_type: Type of content to generate

        Returns:
            Dictionary mapping words to generated content
        """
        results = {}

        for word in words:
            if content_type == "definition":
                results[word] = self.generate_definition(word, grade_level)
            elif content_type == "clue":
                results[word] = self.generate_clue(word, grade_level)
            else:
                results[word] = self.generate_grade_appropriate_content(
                    word, grade_level, content_type
                )

            # Small delay to avoid rate limiting
            time.sleep(0.2)

        return results


# Global instance for easy access
_ai_generator = None

def get_ai_generator() -> AIContentGenerator:
    """Get or create the global AI content generator instance"""
    global _ai_generator
    if _ai_generator is None:
        _ai_generator = AIContentGenerator()
    return _ai_generator

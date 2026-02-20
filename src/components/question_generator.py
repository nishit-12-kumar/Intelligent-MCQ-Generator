# src/components/question_generator.py

import random
import sys
import json
import os

from groq import Groq
from dotenv import load_dotenv

from src.logger.logger import logging
from src.exception.custom_exception import CustomException

load_dotenv()


class QuestionGenerator:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")

        self.client = Groq(api_key=api_key)
        logging.info("Groq client initialized successfully")

    def _generate_mcq_with_groq(self, sentence: str) -> dict:
        prompt = f"""You are an expert MCQ generator. Given the sentence below, generate ONE high-quality multiple choice question.

Rules:
- Question must test understanding, NOT just recall of a word
- Question must be clear and specific
- Provide exactly 4 options
- Only ONE option should be correct
- Wrong options must be plausible but clearly wrong
- Do NOT use fill-in-the-blank style

Sentence: "{sentence}"

Respond in this exact JSON format only, no extra text, no markdown:
{{
  "question": "your question here?",
  "options": ["option A", "option B", "option C", "option D"],
  "correct_answer": "the correct option text here"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            raw = response.choices[0].message.content.strip()

            # Clean markdown if present
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            mcq = json.loads(raw)

            # Validate
            if not all(k in mcq for k in ["question", "options", "correct_answer"]):
                return None
            if len(mcq["options"]) != 4:
                return None
            if mcq["correct_answer"] not in mcq["options"]:
                return None

            return mcq

        except Exception as e:
            logging.warning(f"Groq generation failed: {e}")
            return None

    def generate_mcqs(self, sentences: list, keywords: list, num_questions: int = 5) -> list:
        try:
            logging.info("Starting Groq MCQ generation")

            mcqs = []
            used_sentences = set()

            good_sentences = [
                s for s in sentences
                if len(s.split()) >= 8 and s not in used_sentences
            ]

            for sentence in good_sentences:

                if len(mcqs) >= num_questions:
                    break

                logging.info(f"Generating MCQ for: {sentence[:60]}...")
                mcq = self._generate_mcq_with_groq(sentence)

                if mcq:
                    random.shuffle(mcq["options"])
                    mcqs.append(mcq)
                    used_sentences.add(sentence)

            logging.info(f"Generated {len(mcqs)} MCQs")
            return mcqs

        except Exception as e:
            logging.error("Error in Groq MCQ generation")
            raise CustomException(e, sys)

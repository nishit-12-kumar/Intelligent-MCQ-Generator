# src/pipeline/mcq_pipeline.py

import sys

from src.components.text_cleaner import clean_text, get_sentences
from src.components.question_generator import QuestionGenerator

from src.logger.logger import logging
from src.exception.custom_exception import CustomException


class MCQPipeline:

    def __init__(self):
        self.question_generator = QuestionGenerator()

    def generate_mcqs(self, text: str, num_questions: int = 5) -> list:
        try:
            logging.info("MCQ Pipeline started")

            cleaned_text = clean_text(text)
            sentences = get_sentences(cleaned_text)

            if not sentences:
                logging.warning("No valid sentences found")
                return []

            mcqs = self.question_generator.generate_mcqs(
                sentences=sentences,
                keywords=[],
                num_questions=num_questions
            )

            logging.info("MCQ Pipeline completed successfully")
            return mcqs

        except Exception as e:
            logging.error("Error in MCQ pipeline")
            raise CustomException(e, sys)
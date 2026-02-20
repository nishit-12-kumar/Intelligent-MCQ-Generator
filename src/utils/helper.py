# src/utils/helper.py

import random
import sys
from src.logger.logger import logging
from src.exception.custom_exception import CustomException


def shuffle_options(options: list) -> list:
    """
    Shuffle MCQ options randomly

    Args:
        options (list): List of options

    Returns:
        list: Shuffled options
    """

    try:
        random.shuffle(options)
        return options

    except Exception as e:
        logging.error("Error while shuffling options")
        raise CustomException(e, sys)


def validate_text_input(text: str) -> bool:
    """
    Validate if text input is meaningful

    Args:
        text (str): Input text

    Returns:
        bool: True if valid, False otherwise
    """

    try:
        if not text:
            return False

        if len(text.strip()) < 20:  # Minimum length check
            return False

        return True

    except Exception as e:
        logging.error("Error while validating text input")
        raise CustomException(e, sys)


def format_mcq_output(mcqs: list) -> list:
    """
    Format MCQ output in consistent structure

    Args:
        mcqs (list): List of raw MCQ dictionaries

    Returns:
        list: Formatted MCQs
    """

    try:
        formatted = []

        for idx, mcq in enumerate(mcqs, start=1):
            formatted.append({
                "question_id": idx,
                "question": mcq["question"],
                "options": mcq["options"],
                "correct_answer": mcq["correct_answer"]
            })

        return formatted

    except Exception as e:
        logging.error("Error while formatting MCQ output")
        raise CustomException(e, sys)
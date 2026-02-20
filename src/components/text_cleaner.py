# src/components/text_cleaner.py

import re
import string
import sys
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

from src.logger.logger import logging
from src.exception.custom_exception import CustomException


# Load stopwords once
STOP_WORDS = set(stopwords.words("english"))


def clean_text(text: str) -> str:
    """
    Basic text cleaning:
    - Remove extra spaces
    - Remove special characters
    - Normalize text
    """

    try:
        logging.info("Starting basic text cleaning")

        # Remove newline characters
        text = text.replace("\n", " ")

        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text)

        # Remove unwanted symbols (keep alphabets & numbers)
        text = re.sub(r"[^a-zA-Z0-9.,!? ]+", "", text)

        logging.info("Text cleaning completed")

        return text.strip()

    except Exception as e:
        logging.error("Error in clean_text function")
        raise CustomException(e, sys)


def get_sentences(text: str) -> list:
    """
    Convert paragraph into list of sentences
    """

    try:
        logging.info("Tokenizing text into sentences")

        sentences = sent_tokenize(text)

        return sentences

    except Exception as e:
        logging.error("Error in get_sentences function")
        raise CustomException(e, sys)


def remove_stopwords(sentence: str) -> str:
    """
    Remove stopwords from a single sentence
    """

    try:
        words = word_tokenize(sentence)

        filtered_words = [
            word for word in words
            if word.lower() not in STOP_WORDS
            and word not in string.punctuation
        ]

        return " ".join(filtered_words)

    except Exception as e:
        logging.error("Error in remove_stopwords function")
        raise CustomException(e, sys)
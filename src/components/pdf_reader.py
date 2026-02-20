# src/components/pdf_reader.py

from PyPDF2 import PdfReader
from src.exception.custom_exception import CustomException
from src.logger.logger import logging
import sys


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a given PDF file path.

    Args:
        file_path (str): Path of the uploaded PDF file

    Returns:
        str: Extracted text from PDF
    """
    try:
        logging.info("Starting PDF text extraction")

        reader = PdfReader(file_path)
        text = ""

        for page_number, page in enumerate(reader.pages):
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        logging.info("PDF text extraction completed successfully")

        return text.strip()

    except Exception as e:
        logging.error("Error occurred while extracting text from PDF")
        raise CustomException(e, sys)
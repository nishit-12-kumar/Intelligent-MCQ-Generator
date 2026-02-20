# src/exception/custom_exception.py

import sys
from src.logger.logger import logging


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        """
        Extract detailed error information including
        file name and line number
        """

        _, _, exc_tb = error_detail.exc_info()

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        detailed_error_message = (
            f"Error occurred in script: [{file_name}] "
            f"at line number: [{line_number}] "
            f"with message: [{str(error_message)}]"
        )

        return detailed_error_message

    def __str__(self):
        return self.error_message
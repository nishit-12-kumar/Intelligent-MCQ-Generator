# src/components/text_chunker.py

import sys
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.logger.logger import logging
from src.exception.custom_exception import CustomException


class TextChunker:

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize the text chunker with chunk size and overlap.

        chunk_size: Maximum characters per chunk
        chunk_overlap: Characters shared between consecutive chunks
                       (helps preserve context across chunk boundaries)
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", " "]
        )

    def split_text(self, text: str) -> list:
        """
        Split a large text into smaller overlapping chunks.

        Args:
            text (str): Full extracted text from PDF

        Returns:
            list: List of text chunks
        """
        try:
            logging.info("Starting text chunking")

            if not text or len(text.strip()) == 0:
                logging.warning("Empty text provided for chunking")
                return []

            chunks = self.splitter.split_text(text)

            logging.info(f"Text split into {len(chunks)} chunks")
            return chunks

        except Exception as e:
            logging.error("Error in text chunking")
            raise CustomException(e, sys)
'''

---

**What this does in simple words:**
- Takes the full PDF text (could be 50 pages)
- Splits it into small chunks of **500 characters each**
- Each chunk **overlaps by 50 characters** with the next one — this prevents losing context at chunk boundaries
- Uses smart separators — splits on paragraphs first, then sentences, then words

**Example:**
```
500 page textbook
→ ["Machine learning is...", "Gradient descent is...", "Neural networks are...", ...]
→ 200-300 small chunks


'''
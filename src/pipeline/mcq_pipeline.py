# # src/pipeline/mcq_pipeline.py

# import sys

# from src.components.text_cleaner import clean_text, get_sentences
# from src.components.question_generator import QuestionGenerator

# from src.logger.logger import logging
# from src.exception.custom_exception import CustomException


# class MCQPipeline:

#     def __init__(self):
#         self.question_generator = QuestionGenerator()

#     def generate_mcqs(self, text: str, num_questions: int = 5) -> list:
#         try:
#             logging.info("MCQ Pipeline started")

#             cleaned_text = clean_text(text)
#             sentences = get_sentences(cleaned_text)

#             if not sentences:
#                 logging.warning("No valid sentences found")
#                 return []

#             mcqs = self.question_generator.generate_mcqs(
#                 sentences=sentences,
#                 keywords=[],
#                 num_questions=num_questions
#             )

#             logging.info("MCQ Pipeline completed successfully")
#             return mcqs

#         except Exception as e:
#             logging.error("Error in MCQ pipeline")
#             raise CustomException(e, sys)










# src/pipeline/mcq_pipeline.py

import sys

from src.components.pdf_reader import extract_text_from_pdf
from src.components.text_chunker import TextChunker
from src.components.retriever import Retriever
from src.components.question_generator import QuestionGenerator

from src.logger.logger import logging
from src.exception.custom_exception import CustomException


class MCQPipeline:

    def __init__(self):
        """
        Initialize all RAG pipeline components.
        """
        try:
            logging.info("Initializing RAG MCQ Pipeline")

            self.text_chunker = TextChunker()
            self.retriever = Retriever()
            self.question_generator = QuestionGenerator()

            logging.info("RAG MCQ Pipeline initialized successfully")

        except Exception as e:
            logging.error("Error initializing MCQ Pipeline")
            raise CustomException(e, sys)

    def index_document(self, text: str) -> int:
        """
        Process and index a document (text or PDF content).
        Called ONCE when user uploads a PDF or enters text.

        Args:
            text (str): Full extracted text from PDF or text input

        Returns:
            int: Number of chunks indexed
        """
        try:
            logging.info("Starting document indexing")

            if not text or len(text.strip()) == 0:
                logging.warning("Empty text provided")
                return 0

            # Step 1: Split text into chunks
            chunks = self.text_chunker.split_text(text)

            if not chunks:
                logging.warning("No chunks generated from text")
                return 0

            # Step 2: Generate embeddings and build FAISS index
            self.retriever.index_chunks(chunks)

            logging.info(f"Document indexed successfully with {len(chunks)} chunks")
            return len(chunks)

        except Exception as e:
            logging.error("Error indexing document")
            raise CustomException(e, sys)

    def generate_mcqs(self, topic: str, num_questions: int = 5) -> list:
        """
        Generate MCQs for a given topic using RAG.
        Called every time user enters a topic query.

        Args:
            topic (str): User's topic e.g. "Gradient Descent"
            num_questions (int): Number of MCQs to generate

        Returns:
            list: List of generated MCQs
        """
        try:
            logging.info(f"Generating MCQs for topic: {topic}")

            # Check if document is indexed
            if not self.retriever.is_ready():
                logging.warning("Document not indexed yet")
                return []

            # Step 1: Retrieve relevant chunks for topic
            relevant_chunks = self.retriever.retrieve(
                query=topic,
                top_k=5
            )

            if not relevant_chunks:
                logging.warning(f"No relevant chunks found for topic: {topic}")
                return []

            logging.info(f"Retrieved {len(relevant_chunks)} chunks for topic: {topic}")

            # Step 2: Generate MCQs from retrieved chunks
            mcqs = self.question_generator.generate_mcqs(
                retrieved_chunks=relevant_chunks,
                topic=topic,
                num_questions=num_questions
            )

            logging.info(f"Generated {len(mcqs)} MCQs for topic: {topic}")
            return mcqs

        except Exception as e:
            logging.error("Error generating MCQs")
            raise CustomException(e, sys)

    def is_document_indexed(self) -> bool:
        """
        Check if a document has been indexed and
        the pipeline is ready for MCQ generation.

        Returns:
            bool: True if ready, False otherwise
        """
        return self.retriever.is_ready()


'''
---

**What changed from old `mcq_pipeline.py`:**

| Old Pipeline | New RAG Pipeline |
|---|---|
| `generate_mcqs(text)` — one function | Split into `index_document()` + `generate_mcqs()` |
| Processed text every time | Index **once**, query **many times** |
| No topic awareness | Topic-based retrieval |
| Sent all sentences to Groq | Sends only **relevant chunks** |
| `text_cleaner` + `keyword_extractor` | `text_chunker` + `retriever` |

---

**New Flow:**
```
ONCE:
PDF Upload → index_document() → chunks → embeddings → FAISS index

EVERY QUERY:
User types topic → generate_mcqs(topic)
                 → retrieve relevant chunks
                 → send to Groq
                 → return MCQs


'''



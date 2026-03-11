# src/components/embedding_generator.py

import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

from src.logger.logger import logging
from src.exception.custom_exception import CustomException


class EmbeddingGenerator:

    def __init__(self):
        """
        TF-IDF based embeddings — no torch, no onnx, no DLL issues.
        Pure Python + scikit-learn only.
        """
        self.vectorizer = TfidfVectorizer(
            max_features=512,
            stop_words="english",
            ngram_range=(1, 2)
        )
        self.is_fitted = False
        logging.info("TF-IDF EmbeddingGenerator initialized")

    def generate_embeddings(self, chunks: list) -> np.ndarray:
        """
        Convert list of text chunks into TF-IDF vectors.

        Args:
            chunks (list): List of text chunks

        Returns:
            np.ndarray: Array of embedding vectors
        """
        try:
            logging.info(f"Generating TF-IDF embeddings for {len(chunks)} chunks")

            if not chunks:
                return np.array([])

            embeddings = self.vectorizer.fit_transform(chunks).toarray()
            embeddings = normalize(embeddings, norm="l2")
            self.is_fitted = True

            logging.info(f"Generated {len(embeddings)} embeddings successfully")
            return embeddings.astype("float32")

        except Exception as e:
            logging.error("Error generating embeddings")
            raise CustomException(e, sys)

    def generate_single_embedding(self, text: str) -> np.ndarray:
        """
        Convert a single query into a TF-IDF vector.

        Args:
            text (str): User's topic query

        Returns:
            np.ndarray: Embedding vector
        """
        try:
            logging.info(f"Generating embedding for query: {text[:50]}")

            if not self.is_fitted:
                logging.warning("Vectorizer not fitted yet")
                return np.zeros(512, dtype="float32")

            embedding = self.vectorizer.transform([text]).toarray()
            embedding = normalize(embedding, norm="l2")

            logging.info("Query embedding generated successfully")
            return embedding[0].astype("float32")

        except Exception as e:
            logging.error("Error generating query embedding")
            raise CustomException(e, sys)
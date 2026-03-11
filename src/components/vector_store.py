# src/components/vector_store.py

import sys
import numpy as np
import faiss

from src.logger.logger import logging
from src.exception.custom_exception import CustomException


class VectorStore:

    def __init__(self):
        """
        Initialize empty FAISS vector store.
        FAISS = Facebook AI Similarity Search
        - Runs fully locally
        - Extremely fast similarity search
        - Free and open source
        """
        self.index = None
        self.chunks = []       # stores original text chunks
        self.dimension = None  # embedding dimension (384 for MiniLM)

    def build_index(self, chunks: list, embeddings: np.ndarray) -> None:
        """
        Build FAISS index from chunks and their embeddings.

        Args:
            chunks (list): Original text chunks
            embeddings (np.ndarray): Embedding vectors for each chunk
        """
        try:
            logging.info("Building FAISS index")

            if len(chunks) == 0 or len(embeddings) == 0:
                logging.warning("No chunks or embeddings provided")
                return

            # Store chunks for later retrieval
            self.chunks = chunks

            # Get embedding dimension
            self.dimension = embeddings.shape[1]

            # Convert to float32 (required by FAISS)
            embeddings = np.array(embeddings).astype("float32")

            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)

            # Create FAISS index using Inner Product (cosine similarity)
            self.index = faiss.IndexFlatIP(self.dimension)

            # Add embeddings to index
            self.index.add(embeddings)

            logging.info(f"FAISS index built with {self.index.ntotal} vectors")

        except Exception as e:
            logging.error("Error building FAISS index")
            raise CustomException(e, sys)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list:
        """
        Search for top-k most similar chunks to the query embedding.

        Args:
            query_embedding (np.ndarray): Embedding of user's topic query
            top_k (int): Number of relevant chunks to retrieve

        Returns:
            list: Top-k most relevant text chunks
        """
        try:
            logging.info(f"Searching FAISS index for top {top_k} chunks")

            if self.index is None:
                logging.warning("FAISS index not built yet")
                return []

            # Convert query to float32
            query_embedding = np.array([query_embedding]).astype("float32")

            # Normalize query embedding
            faiss.normalize_L2(query_embedding)

            # Search index
            distances, indices = self.index.search(query_embedding, top_k)

            # Retrieve actual text chunks
            retrieved_chunks = []
            for idx in indices[0]:
                if idx != -1 and idx < len(self.chunks):
                    retrieved_chunks.append(self.chunks[idx])

            logging.info(f"Retrieved {len(retrieved_chunks)} relevant chunks")
            return retrieved_chunks

        except Exception as e:
            logging.error("Error searching FAISS index")
            raise CustomException(e, sys)

    def is_ready(self) -> bool:
        """
        Check if vector store is built and ready for search.

        Returns:
            bool: True if index is ready, False otherwise
        """
        return self.index is not None and len(self.chunks) > 0
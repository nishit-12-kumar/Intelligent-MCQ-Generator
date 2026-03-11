# src/components/retriever.py

import sys

from src.components.embedding_generator import EmbeddingGenerator
from src.components.vector_store import VectorStore

from src.logger.logger import logging
from src.exception.custom_exception import CustomException


class Retriever:

    def __init__(self):
        """
        Initialize Retriever with EmbeddingGenerator and VectorStore.
        This is the core of the RAG pipeline —
        it connects embedding search with vector storage.
        """
        try:
            self.embedding_generator = EmbeddingGenerator()
            self.vector_store = VectorStore()
            logging.info("Retriever initialized successfully")

        except Exception as e:
            logging.error("Error initializing Retriever")
            raise CustomException(e, sys)

    def index_chunks(self, chunks: list) -> None:
        """
        Convert chunks to embeddings and store in FAISS index.
        Called once after PDF is uploaded and chunked.

        Args:
            chunks (list): List of text chunks from PDF
        """
        try:
            logging.info(f"Indexing {len(chunks)} chunks")

            if not chunks:
                logging.warning("No chunks to index")
                return

            # Step 1: Generate embeddings for all chunks
            embeddings = self.embedding_generator.generate_embeddings(chunks)

            # Step 2: Build FAISS index
            self.vector_store.build_index(chunks, embeddings)

            logging.info("Chunks indexed successfully")

        except Exception as e:
            logging.error("Error indexing chunks")
            raise CustomException(e, sys)

    def retrieve(self, query: str, top_k: int = 5) -> list:
        """
        Retrieve most relevant chunks for a given topic query.
        Called every time user enters a topic.

        Args:
            query (str): User's topic query e.g. "Gradient Descent"
            top_k (int): Number of relevant chunks to retrieve

        Returns:
            list: Most relevant text chunks for the query
        """
        try:
            logging.info(f"Retrieving chunks for query: {query}")

            if not self.vector_store.is_ready():
                logging.warning("Vector store not ready — index PDF first")
                return []

            if not query or len(query.strip()) == 0:
                logging.warning("Empty query provided")
                return []

            # Step 1: Convert user query to embedding
            query_embedding = self.embedding_generator.generate_single_embedding(query)

            # Step 2: Search FAISS for similar chunks
            relevant_chunks = self.vector_store.search(
                query_embedding,
                top_k=top_k
            )

            logging.info(f"Retrieved {len(relevant_chunks)} chunks for query: {query}")
            return relevant_chunks

        except Exception as e:
            logging.error("Error retrieving chunks")
            raise CustomException(e, sys)

    def is_ready(self) -> bool:
        """
        Check if retriever is ready to search.

        Returns:
            bool: True if index is built, False otherwise
        """
        return self.vector_store.is_ready()

'''
---

**What this does in simple words:**

`index_chunks()` — called **once** when PDF is uploaded:
```
PDF chunks → Generate embeddings → Store in FAISS
```

`retrieve()` — called **every time** user enters a topic:
```
"Gradient Descent" 
→ Convert to embedding 
→ Search FAISS 
→ Return top 5 relevant chunks
```

`is_ready()` — checks if PDF has been processed:
```
Before PDF upload → False (can't search yet)
After PDF upload  → True (ready to search)
```

---

**How all 4 files connect so far:**
```
PDF Text
   ↓
TextChunker          → ["chunk1", "chunk2", ...]
   ↓
EmbeddingGenerator   → [[0.23, -0.45, ...], ...]
   ↓
VectorStore          → FAISS Index built
   ↓
Retriever            → User query → Top 5 relevant chunks

'''
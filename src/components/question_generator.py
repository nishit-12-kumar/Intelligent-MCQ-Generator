# # src/components/question_generator.py

# import random
# import sys
# import json
# import os

# from groq import Groq
# from dotenv import load_dotenv

# from src.logger.logger import logging
# from src.exception.custom_exception import CustomException

# load_dotenv()


# class QuestionGenerator:

#     def __init__(self):

#         api_key = os.getenv("GROQ_API_KEY")
#         if not api_key:
#             raise ValueError("GROQ_API_KEY not found in .env file")

#         self.client = Groq(api_key=api_key)
#         logging.info("Groq client initialized successfully")

#     def _generate_mcq_with_groq(self, sentence: str) -> dict:
#         prompt = f"""You are an expert MCQ generator. Given the sentence below, generate ONE high-quality multiple choice question.

# Rules:
# - Question must test understanding, NOT just recall of a word
# - Question must be clear and specific
# - Provide exactly 4 options
# - Only ONE option should be correct
# - Wrong options must be plausible but clearly wrong
# - Do NOT use fill-in-the-blank style

# Sentence: "{sentence}"

# Respond in this exact JSON format only, no extra text, no markdown:
# {{
#   "question": "your question here?",
#   "options": ["option A", "option B", "option C", "option D"],
#   "correct_answer": "the correct option text here"
# }}"""

#         try:
#             response = self.client.chat.completions.create(
#                 model="llama-3.3-70b-versatile",
#                 messages=[{"role": "user", "content": prompt}],
#                 temperature=0.7
#             )

#             raw = response.choices[0].message.content.strip()

#             # Clean markdown if present
#             if "```" in raw:
#                 raw = raw.split("```")[1]
#                 if raw.startswith("json"):
#                     raw = raw[4:]
#             raw = raw.strip()

#             mcq = json.loads(raw)

#             # Validate
#             if not all(k in mcq for k in ["question", "options", "correct_answer"]):
#                 return None
#             if len(mcq["options"]) != 4:
#                 return None
#             if mcq["correct_answer"] not in mcq["options"]:
#                 return None

#             return mcq

#         except Exception as e:
#             logging.warning(f"Groq generation failed: {e}")
#             return None

#     def generate_mcqs(self, sentences: list, keywords: list, num_questions: int = 5) -> list:
#         try:
#             logging.info("Starting Groq MCQ generation")

#             mcqs = []
#             used_sentences = set()

#             good_sentences = [
#                 s for s in sentences
#                 if len(s.split()) >= 8 and s not in used_sentences
#             ]

#             for sentence in good_sentences:

#                 if len(mcqs) >= num_questions:
#                     break

#                 logging.info(f"Generating MCQ for: {sentence[:60]}...")
#                 mcq = self._generate_mcq_with_groq(sentence)

#                 if mcq:
#                     random.shuffle(mcq["options"])
#                     mcqs.append(mcq)
#                     used_sentences.add(sentence)

#             logging.info(f"Generated {len(mcqs)} MCQs")
#             return mcqs

#         except Exception as e:
#             logging.error("Error in Groq MCQ generation")
#             raise CustomException(e, sys)











# src/components/question_generator.py

import random
import sys
import json
import os

from groq import Groq
from dotenv import load_dotenv

from src.logger.logger import logging
from src.exception.custom_exception import CustomException

load_dotenv()


class QuestionGenerator:

    def __init__(self):
        """
        Initialize Groq client for LLM-based MCQ generation.
        """
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")

        self.client = Groq(api_key=api_key)
        logging.info("Groq client initialized successfully")

    def _generate_mcq_with_groq(self, context: str, topic: str) -> dict:
        """
        Generate ONE MCQ from retrieved context chunks + user topic.

        Args:
            context (str): Retrieved relevant text chunks joined together
            topic (str): User's topic query e.g. "Gradient Descent"

        Returns:
            dict: MCQ with question, options, correct_answer
        """
        prompt = f"""You are an expert MCQ generator. Using ONLY the context provided below, generate ONE high-quality multiple choice question specifically about the topic: "{topic}".

Context:
{context}

Rules:
- Question must be based STRICTLY on the provided context
- Question must test understanding of "{topic}", NOT just recall of a word
- Question must be clear and specific
- Provide exactly 4 options
- Only ONE option should be correct
- Wrong options must be plausible but clearly wrong
- Do NOT use fill-in-the-blank style
- Do NOT make up information outside the context

Respond in this exact JSON format only, no extra text, no markdown:
{{
  "question": "your question here?",
  "options": ["option A", "option B", "option C", "option D"],
  "correct_answer": "the correct option text here"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            raw = response.choices[0].message.content.strip()

            # Clean markdown code blocks if present
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            mcq = json.loads(raw)

            # Validate structure
            if not all(k in mcq for k in ["question", "options", "correct_answer"]):
                logging.warning("Invalid MCQ structure from Groq")
                return None

            if len(mcq["options"]) != 4:
                logging.warning("MCQ does not have 4 options")
                return None

            if mcq["correct_answer"] not in mcq["options"]:
                logging.warning("Correct answer not in options")
                return None

            return mcq

        except Exception as e:
            logging.warning(f"Groq generation failed: {e}")
            return None

    def generate_mcqs(self, retrieved_chunks: list, topic: str, num_questions: int = 5) -> list:
        """
        Generate multiple MCQs from retrieved RAG chunks.

        Args:
            retrieved_chunks (list): Relevant chunks from FAISS retrieval
            topic (str): User's topic query
            num_questions (int): Number of MCQs to generate

        Returns:
            list: List of MCQ dictionaries
        """
        try:
            logging.info(f"Generating {num_questions} MCQs for topic: {topic}")

            if not retrieved_chunks:
                logging.warning("No chunks provided for MCQ generation")
                return []

            mcqs = []

            # Strategy: use different chunks for different questions
            # to ensure variety in MCQs
            for i in range(num_questions):

                if not retrieved_chunks:
                    break

                # Rotate through chunks for variety
                # Use 2 chunks per question for richer context
                chunk_index = i % len(retrieved_chunks)
                next_index = (i + 1) % len(retrieved_chunks)

                # Combine 2 chunks for better context
                context = retrieved_chunks[chunk_index]
                if len(retrieved_chunks) > 1:
                    context = retrieved_chunks[chunk_index] + "\n\n" + retrieved_chunks[next_index]

                logging.info(f"Generating MCQ {i+1}/{num_questions}")
                mcq = self._generate_mcq_with_groq(context, topic)

                if mcq:
                    # Avoid duplicate questions
                    if mcq["question"] not in [m["question"] for m in mcqs]:
                        random.shuffle(mcq["options"])
                        mcqs.append(mcq)

            logging.info(f"Successfully generated {len(mcqs)} MCQs for topic: {topic}")
            return mcqs

        except Exception as e:
            logging.error("Error in MCQ generation")
            raise CustomException(e, sys)
'''

---

**Key difference from old version:**

| Old `question_generator.py` | New `question_generator.py` |
|---|---|
| Sent random sentences to Groq | Sends **topic-relevant chunks** to Groq |
| No topic awareness | Generates MCQs **specifically about user's topic** |
| Generic questions | **Context-grounded** questions |
| One sentence per MCQ | **Two chunks combined** for richer context |
| `keywords` parameter used | `retrieved_chunks + topic` used |

---

**How the prompt changed:**
```
OLD: "Generate a MCQ from this sentence"

NEW: "Generate a MCQ about TOPIC X 
      using ONLY this retrieved context"

'''
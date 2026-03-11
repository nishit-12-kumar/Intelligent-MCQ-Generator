# # streamlit_app.py

# import streamlit as st
# from src.pipeline.mcq_pipeline import MCQPipeline
# from src.components.pdf_reader import extract_text_from_pdf
# from src.utils.helper import validate_text_input, format_mcq_output

# import tempfile
# import os
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')


# st.set_page_config(page_title="MCQ Generator", layout="wide")

# st.title("🧠 Intelligent MCQ Generator")
# st.write("Generate MCQs from Text or PDF using AI")

# pipeline = MCQPipeline()


# def clear_mcq_state():
#     """Clear all MCQ related session state keys"""
#     keys_to_delete = [k for k in st.session_state
#                       if any(k.startswith(p) for p in ("text_", "pdf_"))]
#     for k in keys_to_delete:
#         del st.session_state[k]


# def display_mcqs(formatted, tab="text"):
#     """Display MCQs with interactive options and persistent feedback"""

#     for mcq in formatted:
#         st.subheader(f"Q{mcq['question_id']}: {mcq['question']}")

#         # Unique keys per tab to avoid DuplicateWidgetID
#         qid           = f"{tab}_q_{mcq['question_id']}"
#         submitted_key = f"{tab}_submitted_{mcq['question_id']}"
#         selected_key  = f"{tab}_selected_{mcq['question_id']}"

#         # Initialize state
#         if submitted_key not in st.session_state:
#             st.session_state[submitted_key] = False
#         if selected_key not in st.session_state:
#             st.session_state[selected_key] = None

#         # Determine radio index
#         if st.session_state[submitted_key] and st.session_state[selected_key] in mcq["options"]:
#             radio_index = mcq["options"].index(st.session_state[selected_key])
#         else:
#             radio_index = None

#         # Show radio — disabled after submit
#         selected = st.radio(
#             "Choose your answer:",
#             options=mcq["options"],
#             index=radio_index,
#             key=qid,
#             disabled=st.session_state[submitted_key]
#         )

#         # Show submit button only before submission
#         if not st.session_state[submitted_key]:
#             if st.button("Submit", key=f"{tab}_btn_{mcq['question_id']}"):
#                 if selected is None:
#                     st.warning("⚠️ Please select an option first!")
#                 else:
#                     st.session_state[selected_key] = selected
#                     st.session_state[submitted_key] = True

#         # Show feedback after submission
#         if st.session_state[submitted_key]:
#             saved = st.session_state[selected_key]
#             if saved == mcq["correct_answer"]:
#                 st.success("✅ Correct!")
#             else:
#                 st.error("❌ Wrong!")
#                 st.info(f"💡 Correct Answer: **{mcq['correct_answer']}**")

#         st.divider()


# tab1, tab2 = st.tabs(["📄 Enter Text", "📑 Upload PDF"])


# # ------------------ TEXT TAB ------------------ #
# with tab1:

#     user_text = st.text_area("Enter your text here:", height=250)

#     if st.button("Generate MCQs from Text"):

#         if not validate_text_input(user_text):
#             st.warning("Please enter meaningful text (at least 20 characters).")
#         else:
#             with st.spinner("Generating MCQs..."):
#                 mcqs = pipeline.generate_mcqs(user_text)
#                 formatted = format_mcq_output(mcqs)

#                 if not formatted:
#                     st.error("No MCQs generated. Try richer content.")
#                 else:
#                     clear_mcq_state()
#                     st.session_state["formatted_mcqs_text"] = formatted
#                     st.success(f"Generated {len(formatted)} MCQs!")

#     if "formatted_mcqs_text" in st.session_state:
#         display_mcqs(st.session_state["formatted_mcqs_text"], tab="text")


# # ------------------ PDF TAB ------------------ #
# with tab2:

#     uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

#     if st.button("Generate MCQs from PDF"):

#         if uploaded_file is None:
#             st.warning("Please upload a PDF file.")
#         else:
#             with st.spinner("Processing PDF..."):

#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#                     tmp_file.write(uploaded_file.read())
#                     temp_path = tmp_file.name

#                 text = extract_text_from_pdf(temp_path)
#                 os.remove(temp_path)

#                 if not validate_text_input(text):
#                     st.error("PDF does not contain enough readable text.")
#                 else:
#                     mcqs = pipeline.generate_mcqs(text)
#                     formatted = format_mcq_output(mcqs)

#                     if not formatted:
#                         st.error("No MCQs generated from this PDF.")
#                     else:
#                         clear_mcq_state()
#                         st.session_state["formatted_mcqs_pdf"] = formatted
#                         st.success(f"Generated {len(formatted)} MCQs!")

#     if "formatted_mcqs_pdf" in st.session_state:
#         display_mcqs(st.session_state["formatted_mcqs_pdf"], tab="pdf")










# streamlit_app.py

import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

import streamlit as st
from src.pipeline.mcq_pipeline import MCQPipeline
from src.components.pdf_reader import extract_text_from_pdf
from src.utils.helper import validate_text_input, format_mcq_output

import tempfile
import os

st.set_page_config(page_title="RAG MCQ Generator", layout="wide")

st.title("🧠 RAG-Based Intelligent MCQ Generator")
st.write("Upload a PDF or enter text → Enter a topic → Get AI-generated MCQs")

# Initialize pipeline once
if "pipeline" not in st.session_state:
    st.session_state["pipeline"] = MCQPipeline()

pipeline = st.session_state["pipeline"]


# ---------------------- HELPER FUNCTIONS ---------------------- #

def clear_mcq_state():
    """Clear all MCQ related session state keys"""
    keys_to_delete = [k for k in st.session_state
                      if any(k.startswith(p) for p in ("text_", "pdf_"))]
    for k in keys_to_delete:
        del st.session_state[k]


def display_mcqs(formatted, tab="text"):
    """Display MCQs with interactive options and persistent feedback"""

    for mcq in formatted:
        st.subheader(f"Q{mcq['question_id']}: {mcq['question']}")

        qid           = f"{tab}_q_{mcq['question_id']}"
        submitted_key = f"{tab}_submitted_{mcq['question_id']}"
        selected_key  = f"{tab}_selected_{mcq['question_id']}"

        if submitted_key not in st.session_state:
            st.session_state[submitted_key] = False
        if selected_key not in st.session_state:
            st.session_state[selected_key] = None

        # Determine radio index
        if st.session_state[submitted_key] and st.session_state[selected_key] in mcq["options"]:
            radio_index = mcq["options"].index(st.session_state[selected_key])
        else:
            radio_index = None

        # Show radio — disabled after submit
        selected = st.radio(
            "Choose your answer:",
            options=mcq["options"],
            index=radio_index,
            key=qid,
            disabled=st.session_state[submitted_key]
        )

        # Show submit button only before submission
        if not st.session_state[submitted_key]:
            if st.button("Submit", key=f"{tab}_btn_{mcq['question_id']}"):
                if selected is None:
                    st.warning("⚠️ Please select an option first!")
                else:
                    st.session_state[selected_key] = selected
                    st.session_state[submitted_key] = True

        # Show feedback after submission
        if st.session_state[submitted_key]:
            saved = st.session_state[selected_key]
            if saved == mcq["correct_answer"]:
                st.success("✅ Correct!")
            else:
                st.error("❌ Wrong!")
                st.info(f"💡 Correct Answer: **{mcq['correct_answer']}**")

        st.divider()


# ---------------------- TABS ---------------------- #

tab1, tab2 = st.tabs(["📄 Enter Text", "📑 Upload PDF"])


# ------------------ TEXT TAB ------------------ #
with tab1:

    user_text = st.text_area("Enter your text here:", height=250)

    # Step 1 — Index document
    if st.button("Process Text"):
        if not validate_text_input(user_text):
            st.warning("Please enter meaningful text (at least 20 characters).")
        else:
            with st.spinner("Processing and indexing text..."):
                num_chunks = pipeline.index_document(user_text)
                if num_chunks == 0:
                    st.error("Could not process text. Try richer content.")
                else:
                    st.session_state["text_indexed"] = True
                    st.session_state["text_num_chunks"] = num_chunks
                    st.success(f"✅ Text processed! Indexed {num_chunks} chunks. Now enter a topic below.")

    # Step 2 — Enter topic and generate MCQs
    if st.session_state.get("text_indexed"):
        st.info(f"📚 Document indexed with **{st.session_state.get('text_num_chunks', 0)}** chunks — Ready for queries!")

        topic = st.text_input(
            "Enter a topic to generate MCQs about:",
            placeholder="e.g. Gradient Descent, Neural Networks, Cricket IPL...",
            key="text_topic"
        )

        col1, col2 = st.columns([1, 5])
        with col1:
            num_q = st.selectbox("No. of MCQs", [3, 5, 7, 10], index=1, key="text_num_q")

        if st.button("Generate MCQs", key="text_generate"):
            if not topic or len(topic.strip()) == 0:
                st.warning("⚠️ Please enter a topic first!")
            else:
                with st.spinner(f"Retrieving relevant content and generating MCQs on '{topic}'..."):
                    mcqs = pipeline.generate_mcqs(
                        topic=topic,
                        num_questions=num_q
                    )
                    formatted = format_mcq_output(mcqs)

                    if not formatted:
                        st.error(f"No MCQs generated for topic '{topic}'. Try a different topic.")
                    else:
                        clear_mcq_state()
                        st.session_state["formatted_mcqs_text"] = formatted
                        st.success(f"Generated {len(formatted)} MCQs on '{topic}'!")

    # Display MCQs
    if "formatted_mcqs_text" in st.session_state:
        display_mcqs(st.session_state["formatted_mcqs_text"], tab="text")


# ------------------ PDF TAB ------------------ #
with tab2:

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Step 1 — Process PDF
    if st.button("Process PDF"):
        if uploaded_file is None:
            st.warning("Please upload a PDF file first.")
        else:
            with st.spinner("Extracting and indexing PDF..."):

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    temp_path = tmp_file.name

                text = extract_text_from_pdf(temp_path)
                os.remove(temp_path)

                if not validate_text_input(text):
                    st.error("PDF does not contain enough readable text.")
                else:
                    num_chunks = pipeline.index_document(text)
                    if num_chunks == 0:
                        st.error("Could not process PDF. Try a different file.")
                    else:
                        st.session_state["pdf_indexed"] = True
                        st.session_state["pdf_num_chunks"] = num_chunks
                        st.success(f"✅ PDF processed! Indexed {num_chunks} chunks. Now enter a topic below.")

    # Step 2 — Enter topic and generate MCQs
    if st.session_state.get("pdf_indexed"):
        st.info(f"📚 PDF indexed with **{st.session_state.get('pdf_num_chunks', 0)}** chunks — Ready for queries!")

        topic = st.text_input(
            "Enter a topic to generate MCQs about:",
            placeholder="e.g. Machine Learning, Data Structures, History...",
            key="pdf_topic"
        )

        col1, col2 = st.columns([1, 5])
        with col1:
            num_q = st.selectbox("No. of MCQs", [3, 5, 7, 10], index=1, key="pdf_num_q")

        if st.button("Generate MCQs", key="pdf_generate"):
            if not topic or len(topic.strip()) == 0:
                st.warning("⚠️ Please enter a topic first!")
            else:
                with st.spinner(f"Retrieving relevant content and generating MCQs on '{topic}'..."):
                    mcqs = pipeline.generate_mcqs(
                        topic=topic,
                        num_questions=num_q
                    )
                    formatted = format_mcq_output(mcqs)

                    if not formatted:
                        st.error(f"No MCQs generated for topic '{topic}'. Try a different topic.")
                    else:
                        clear_mcq_state()
                        st.session_state["formatted_mcqs_pdf"] = formatted
                        st.success(f"Generated {len(formatted)} MCQs on '{topic}'!")

    # Display MCQs
    if "formatted_mcqs_pdf" in st.session_state:
        display_mcqs(st.session_state["formatted_mcqs_pdf"], tab="pdf")


'''

---

**What changed in the UI:**

| Old UI | New RAG UI |
|---|---|
| One button — Generate MCQs | Two steps — **Process** then **Generate** |
| No topic input | **Topic input box** added |
| Generated from all text | Generated from **retrieved relevant chunks** |
| Fixed 5 questions | User can select **3, 5, 7, or 10** questions |
| No document status | Shows **chunks indexed** count |

---

**New User Flow:**
```
Tab 1 - Text:
1. Paste text → Click "Process Text"
2. Enter topic → Select no. of MCQs → Click "Generate MCQs"
3. Answer questions with radio buttons

Tab 2 - PDF:
1. Upload PDF → Click "Process PDF"
2. Enter topic → Select no. of MCQs → Click "Generate MCQs"
3. Answer questions with radio buttons
    

'''
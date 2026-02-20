# streamlit_app.py

import streamlit as st
from src.pipeline.mcq_pipeline import MCQPipeline
from src.components.pdf_reader import extract_text_from_pdf
from src.utils.helper import validate_text_input, format_mcq_output

import tempfile
import os

st.set_page_config(page_title="MCQ Generator", layout="wide")

st.title("🧠 Intelligent MCQ Generator")
st.write("Generate MCQs from Text or PDF using AI")

pipeline = MCQPipeline()


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

        # Unique keys per tab to avoid DuplicateWidgetID
        qid           = f"{tab}_q_{mcq['question_id']}"
        submitted_key = f"{tab}_submitted_{mcq['question_id']}"
        selected_key  = f"{tab}_selected_{mcq['question_id']}"

        # Initialize state
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


tab1, tab2 = st.tabs(["📄 Enter Text", "📑 Upload PDF"])


# ------------------ TEXT TAB ------------------ #
with tab1:

    user_text = st.text_area("Enter your text here:", height=250)

    if st.button("Generate MCQs from Text"):

        if not validate_text_input(user_text):
            st.warning("Please enter meaningful text (at least 20 characters).")
        else:
            with st.spinner("Generating MCQs..."):
                mcqs = pipeline.generate_mcqs(user_text)
                formatted = format_mcq_output(mcqs)

                if not formatted:
                    st.error("No MCQs generated. Try richer content.")
                else:
                    clear_mcq_state()
                    st.session_state["formatted_mcqs_text"] = formatted
                    st.success(f"Generated {len(formatted)} MCQs!")

    if "formatted_mcqs_text" in st.session_state:
        display_mcqs(st.session_state["formatted_mcqs_text"], tab="text")


# ------------------ PDF TAB ------------------ #
with tab2:

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if st.button("Generate MCQs from PDF"):

        if uploaded_file is None:
            st.warning("Please upload a PDF file.")
        else:
            with st.spinner("Processing PDF..."):

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    temp_path = tmp_file.name

                text = extract_text_from_pdf(temp_path)
                os.remove(temp_path)

                if not validate_text_input(text):
                    st.error("PDF does not contain enough readable text.")
                else:
                    mcqs = pipeline.generate_mcqs(text)
                    formatted = format_mcq_output(mcqs)

                    if not formatted:
                        st.error("No MCQs generated from this PDF.")
                    else:
                        clear_mcq_state()
                        st.session_state["formatted_mcqs_pdf"] = formatted
                        st.success(f"Generated {len(formatted)} MCQs!")

    if "formatted_mcqs_pdf" in st.session_state:
        display_mcqs(st.session_state["formatted_mcqs_pdf"], tab="pdf")






# # streamlit_app.py

# import streamlit as st
# from src.pipeline.mcq_pipeline import MCQPipeline
# from src.components.pdf_reader import extract_text_from_pdf
# from src.utils.helper import validate_text_input, format_mcq_output

# import tempfile
# import os

# st.set_page_config(page_title="MCQ Generator", layout="wide")

# st.title("🧠 Intelligent MCQ Generator")
# st.write("Generate MCQs from Text or PDF using AI")

# pipeline = MCQPipeline()

# tab1, tab2 = st.tabs(["📄 Enter Text", "📑 Upload PDF"])


# # def display_mcqs(formatted):
# #     for mcq in formatted:
# #         st.subheader(f"Q{mcq['question_id']}: {mcq['question']}")

# #         selected = st.radio(
# #             "Choose your answer:",
# #             options=mcq["options"],
# #             index=None,  # 👈 no auto-selection
# #             key=f"q_{mcq['question_id']}"
# #         )

# #         if st.button("Submit", key=f"btn_{mcq['question_id']}"):
# #             if selected is None:
# #                 st.warning("⚠️ Please select an option first!")
# #             elif selected == mcq["correct_answer"]:
# #                 st.success("✅ Correct!")
# #             else:
# #                 st.error("❌ Wrong!")
# #                 st.info(f"💡 Correct Answer: **{mcq['correct_answer']}**")

# #         st.divider()

# def display_mcqs(formatted):
#     for mcq in formatted:
#         st.subheader(f"Q{mcq['question_id']}: {mcq['question']}")

#         qid = f"q_{mcq['question_id']}"
#         submitted_key = f"submitted_{mcq['question_id']}"
#         selected_key = f"selected_{mcq['question_id']}"

#         # Initialize state
#         if submitted_key not in st.session_state:
#             st.session_state[submitted_key] = False
#         if selected_key not in st.session_state:
#             st.session_state[selected_key] = None

#         # Always show radio — disable after submit
#         selected = st.radio(
#             "Choose your answer:",
#             options=mcq["options"],
#             index=None if not st.session_state[submitted_key]
#                   else mcq["options"].index(st.session_state[selected_key]),
#             key=qid,
#             disabled=st.session_state[submitted_key]
#         )

#         # Show submit button only if not yet submitted
#         if not st.session_state[submitted_key]:
#             if st.button("Submit", key=f"btn_{mcq['question_id']}"):
#                 if selected is None:
#                     st.warning("⚠️ Please select an option first!")
#                 else:
#                     st.session_state[selected_key] = selected
#                     st.session_state[submitted_key] = True

#         # Show feedback if submitted
#         if st.session_state[submitted_key]:
#             saved = st.session_state[selected_key]
#             if saved == mcq["correct_answer"]:
#                 st.success("✅ Correct!")
#             else:
#                 st.error("❌ Wrong!")
#                 st.info(f"💡 Correct Answer: **{mcq['correct_answer']}**")

#         st.divider()


# # Add this helper function at the top, before the tabs
# def clear_mcq_state():
#     keys_to_delete = [k for k in st.session_state if k.startswith(("submitted_", "selected_", "q_", "static_"))]
#     for k in keys_to_delete:
#         del st.session_state[k]


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
#                     st.success(f"Generated {len(formatted)} MCQs!")
#                     clear_mcq_state()
#                     st.session_state["formatted_mcqs_text"] = formatted

#     # Display MCQs outside spinner so they persist after submit
#     if "formatted_mcqs_text" in st.session_state:
#         display_mcqs(st.session_state["formatted_mcqs_text"])


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
#                         st.success(f"Generated {len(formatted)} MCQs!")
#                         clear_mcq_state()
#                         st.session_state["formatted_mcqs_pdf"] = formatted

#     # Display MCQs outside spinner so they persist after submit
#     if "formatted_mcqs_pdf" in st.session_state:
#         display_mcqs(st.session_state["formatted_mcqs_pdf"])
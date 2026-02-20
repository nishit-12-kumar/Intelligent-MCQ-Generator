# 🧠 Intelligent MCQ Generator

An AI-powered Multiple Choice Question (MCQ) generator that takes text or PDF input and generates high-quality questions using the **Groq AI API (Llama 3 model)**.

Built with **Python**, **Streamlit**, and **Groq AI**.

---

## 🚀 Live Demo

👉 [Click here to try the app](https://intelligent-mcq-generator-8nk3icmu88qymuy8n36dxe.streamlit.app/)

---

## 📌 Features

- 📄 Generate MCQs from plain text input
- 📑 Generate MCQs from uploaded PDF files
- 🤖 AI-powered questions using Groq (Llama 3) — not fill-in-the-blank
- ✅ Interactive quiz interface with instant feedback

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| Groq API (Llama 3) | MCQ generation |
| NLTK | Text cleaning and sentence splitting |
| PyPDF2 | PDF text extraction |

---

## 📁 Project Structure

```
mcq_generator/
│
├── streamlit_app.py                  ← Main UI file
│
├── src/
│   ├── pipeline/
│   │   └── mcq_pipeline.py           ← Connects all components
│   │
│   ├── components/
│   │   ├── text_cleaner.py           ← Cleans and splits text into sentences
│   │   ├── question_generator.py     ← Sends sentences to Groq AI, gets MCQs
│   │   └── pdf_reader.py             ← Extracts text from PDF files
│   │
│   ├── utils/
│   │   └── helper.py                 ← Input validation and output formatting
│   │
│   ├── exception/
│   │   └── custom_exception.py       ← Custom error messages with file + line info
│   │
│   └── logger/
│       └── logger.py                 ← Logs all events with timestamps
│
├── .env                              ← API keys (never pushed to GitHub)
└── requirements.txt                  ← Required packages
```

---

## ⚙️ How It Works

```
User Input (Text or PDF)
        ↓
  text_cleaner.py        → Clean text + split into sentences
        ↓
  question_generator.py  → Send each sentence to Groq AI
        ↓
  Groq AI (Llama 3)      → Returns MCQ with 4 options
        ↓
  helper.py              → Format and number the questions
        ↓
  streamlit_app.py       → Display to user with radio buttons
```

---

## 🔧 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/nishit-12-kumar/intelligent-mcq-generator.git
cd intelligent-mcq-generator
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get your free Groq API key
- Go to [https://console.groq.com](https://console.groq.com)
- Sign up and create a free API key

### 5. Create a `.env` file in the project root
```
GROQ_API_KEY=your_groq_api_key_here
```

### 6. Run the app
```bash
streamlit run streamlit_app.py
```

---

## 🙌 Acknowledgements

- [Groq](https://groq.com) — for the free and fast LLM API
- [Streamlit](https://streamlit.io) — for the easy web app framework
- [NLTK](https://www.nltk.org) — for text processing utilities

---

## 👨‍💻 Author

**Nishit Kumar**  
[GitHub](https://github.com/nishit-12-kumar)

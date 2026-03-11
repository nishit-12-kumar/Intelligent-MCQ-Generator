# 🧠 RAG-Based Intelligent MCQ Generator

An AI-powered **Retrieval Augmented Generation (RAG)** based MCQ generator that allows users to upload any PDF or paste text, enter a specific topic, and get high-quality AI-generated MCQs focused **only on that topic** — powered by **Groq API (LLaMA 3)** and **FAISS vector search**.

---

## 🚀 Live Demo

👉 [Click here to try the app](https://intelligent-mcq-generator.streamlit.app)

---

## 📌 Features

- 📄 Generate topic-specific MCQs from plain text input
- 📑 Generate topic-specific MCQs from uploaded PDF files
- 🔍 RAG-based retrieval — fetches **only relevant content** for the topic
- 🤖 AI-powered questions using **Groq API (LLaMA 3)**
- 🗃️ FAISS vector database for fast similarity search
- ✅ Interactive quiz interface with instant feedback
- 🔒 Options lock after submission — answers persist across questions
- 💡 Shows correct answer when wrong option is selected
- 🎯 Select number of MCQs — 3, 5, 7, or 10

---

## 🆚 Why RAG-Based is Better

| Normal MCQ Generator | RAG-Based MCQ Generator |
|---|---|
| Random questions from random sentences | Topic-specific focused questions |
| Sends all text to LLM | Sends only relevant chunks |
| No document memory | Indexes once, query many times |
| Generic low-quality questions | Context-grounded high-quality questions |
| One fixed topic | User chooses any topic from document |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| Groq API (LLaMA 3) | MCQ generation |
| FAISS | Vector similarity search |
| TF-IDF (scikit-learn) | Text embeddings |
| LangChain | Smart text chunking |
| PyPDF2 | PDF text extraction |
| NLTK | Text preprocessing |

---

## 📁 Project Structure

```
mcq_generator/
│
├── streamlit_app.py                    ← Main UI file
│
├── src/
│   ├── pipeline/
│   │   └── mcq_pipeline.py             ← Connects all RAG components
│   │
│   ├── components/
│   │   ├── pdf_reader.py               ← Extracts text from PDF
│   │   ├── text_chunker.py             ← Splits text into smart chunks
│   │   ├── embedding_generator.py      ← Converts chunks to TF-IDF vectors
│   │   ├── vector_store.py             ← Stores and searches vectors via FAISS
│   │   ├── retriever.py                ← Finds relevant chunks for topic
│   │   └── question_generator.py       ← Sends chunks to Groq, gets MCQs
│   │
│   ├── utils/
│   │   └── helper.py                   ← Input validation and formatting
│   │
│   ├── exception/
│   │   └── custom_exception.py         ← Custom error messages
│   │
│   └── logger/
│       └── logger.py                   ← Logs all events with timestamps
│
├── .env                                ← API keys (never pushed to GitHub)
└── requirements.txt                    ← Required packages
```

---

## ⚙️ How It Works

```
STEP 1 — Index Document (runs ONCE):
PDF/Text → TextChunker → chunks
                              ↓
                    EmbeddingGenerator → TF-IDF vectors
                              ↓
                        VectorStore → FAISS Index built

STEP 2 — Generate MCQs (runs on every topic query):
User types topic → Retriever → search FAISS → top 5 relevant chunks
                                                        ↓
                                            QuestionGenerator
                                                        ↓
                                            Groq API (LLaMA 3)
                                                        ↓
                                            Focused MCQs on topic
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

## 📦 Requirements

```
python-dotenv==1.0.1
nltk==3.8.1
PyPDF2==3.0.1
streamlit==1.35.0
groq
requests==2.31.0
langchain==0.2.17
langchain-community==0.2.19
faiss-cpu==1.8.0
scikit-learn==1.4.2
numpy==1.26.4
```

---

## 💻 Usage

### Step 1 — Upload PDF or Enter Text
- Go to **"Enter Text"** tab and paste any text
- OR go to **"Upload PDF"** tab and upload a PDF file

### Step 2 — Process Document
- Click **"Process Text"** or **"Process PDF"**
- System splits document into chunks and builds FAISS index
- You'll see how many chunks were indexed

### Step 3 — Enter Topic and Generate MCQs
- Type a topic in the text box (e.g. *"Gradient Descent"*, *"IPL Cricket"*)
- Select number of MCQs (3, 5, 7, or 10)
- Click **"Generate MCQs"**

### Step 4 — Answer the Quiz
- Select an option for each question
- Click **Submit** to see if you're correct
- Wrong answers show the correct answer in blue

---

## 🌐 Deploying on Streamlit Cloud

1. Push your code to GitHub (make sure `.env` is in `.gitignore`)
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **"New app"** → Select your repo → Set main file as `streamlit_app.py`
4. Go to **Advanced settings → Secrets** and add:
```
GROQ_API_KEY = "your_groq_api_key_here"
```
5. Click **Deploy** 🚀

---

## 🙌 Acknowledgements

- [Groq](https://groq.com) — for the free and fast LLM API
- [Meta LLaMA 3](https://llama.meta.com) — for the powerful open-source LLM
- [FAISS](https://github.com/facebookresearch/faiss) — for fast vector similarity search
- [LangChain](https://langchain.com) — for smart text splitting utilities
- [Streamlit](https://streamlit.io) — for the easy web app framework

---

## 👨‍💻 Author

**Nishit Kumar**
[GitHub](https://github.com/nishit-12-kumar) | [LinkedIn](https://www.linkedin.com/in/nishit-kumar)
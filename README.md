# 📚 Know your PDF — RAG Assistant

A Retrieval-Augmented Generation (RAG) chatbot that lets you upload any PDF and ask questions about it. Built with Streamlit, Qdrant, and Llama 3.1 8B (via Groq).

## How it works

```
PDF upload
  → extract text per page        (PyMuPDF)
  → chunk into 1000-token pieces (LangChain RecursiveCharacterTextSplitter)
  → embed each chunk             (BAAI/bge-small-en-v1.5 — 384 dimensions)
  → store vectors + metadata     (Qdrant)

User question
  → embed question               (same model)
  → cosine similarity search     (Qdrant, top-5 chunks)
  → build prompt: context + chat history + question
  → generate answer              (Llama 3.1 8B via Groq)
  → show answer + source pages
```

---

## Tech stack

| Layer            |          Tool         |
|------------------|-----------------------|
|        UI        |       Streamlit       |
|    PDF parsing   |    PyMuPDF (`fitz`)   |
|     Chunking     | LangChain `RecursiveCharacterTextSplitter` |
| Embedding model  | `BAAI/bge-small-en-v1.5` (local, 384d) |
| Vector database  |         Qdrant        |
|        LLM       | Llama 3.1 8B Instant via Groq API |
| Containerisation | Docker + Docker Compose |

---

## Project structure

```
rag-asst/
├── app.py                  # Streamlit UI — main entry point
├── rag/
│   ├── pdf_loader.py       # Extract text from PDF pages
│   ├── chunker.py          # Split pages into overlapping chunks
│   ├── embeddings.py       # Embed text using BGE-small
│   ├── vector_store.py     # Qdrant collection + upsert
│   ├── retriever.py        # Similarity search against Qdrant
│   └── llm.py              # Groq API call to Llama 3.1 8B
├── docker-compose.yml      # Runs Qdrant + the app together
├── dockerfile              # App container definition
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── .gitignore
```

---

## Prerequisites

- Python 3.11+
- Docker + Docker Compose (for running Qdrant)
- A free [Groq API key](https://console.groq.com)

---

## Setup

### 1. Clone and install

```bash
git clone <your-repo-url>
cd rag-asst
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# open .env and paste your Groq API key
```

### 3. Start Qdrant

```bash
docker-compose up qdrant -d
```

Qdrant will be available at `http://localhost:6333`.

### 4. Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Run everything with Docker

To run both Qdrant and the app in containers:

```bash
docker-compose up --build
```

Then open `http://localhost:8501`.

---

## Usage

1. Upload a PDF using the file uploader.
2. Wait for the **"Indexed N chunks"** confirmation.
3. Type your question in the chat box.
4. The answer will appear with source page references below it.
5. Click **New Chat** in the sidebar to reset the conversation.

---

## Configuration

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key — get one free at console.groq.com |

Chunking parameters (`chunk_size`, `chunk_overlap`) can be adjusted in `rag/chunker.py`.
Qdrant host/port can be changed in `rag/vector_store.py`.

---

## Dependencies

```
streamlit
groq
qdrant-client
sentence-transformers
pymupdf
langchain
langchain-text-splitters
python-dotenv
```

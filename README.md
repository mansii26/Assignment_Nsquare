# 📄 PDF-QA Assistant (RAG + Gemini + HuggingFace)

This is an end-to-end PDF Question Answering system that allows users to upload large PDF files and ask context-aware questions using Google Gemini Pro and HuggingFace sentence embeddings. Built using FastAPI for backend and Streamlit for frontend.

---

## 🚀 Features

- ✅ Upload any PDF file (even large ones)
- ✅ Text chunking using LangChain
- ✅ FAISS VectorStore for semantic search
- ✅ HuggingFace Embeddings (`all-MiniLM-L6-v2`) – **free**
- ✅ Gemini Pro (`gemini-pro`) for answer generation
- ✅ Chat-like Q&A interface (via Streamlit)
- ✅ RAG (Retrieval-Augmented Generation) pipeline
- ✅ Tested on a **500+ page PDF** book

---

## 📦 Tech Stack

| Layer       | Tool                             |
|-------------|----------------------------------|
| Backend     | FastAPI                          |
| Frontend    | Streamlit|
| Embeddings  | HuggingFace (Sentence Transformers) |
| LLM         | Google Gemini (`gemini-pro`)     |
| Vector DB   | FAISS                            |
| Text Split  | LangChain                        |

---
pdf_qa/
│
├── backend/
│ └── main.py # FastAPI app (API for upload & ask)
│
├── app.py # Streamlit frontend (chat-like UI)
├── .gitignore
├── requirements.txt
└── README.md




---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/mansii26/Assignment_Nsquare.git
cd Assignment_Nsquare

## 📁 Folder Structure


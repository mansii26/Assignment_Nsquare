from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use HuggingFace for FREE embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend access (e.g., Streamlit/Gradio/React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global vectorstore
vectorstore = None

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file. Embeds and stores chunks in FAISS.
    """
    reader = PdfReader(file.file)
    raw_text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            raw_text += content

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(raw_text)

    # Store in FAISS vectorstore
    global vectorstore
    vectorstore = FAISS.from_texts(texts, embeddings)

    return {"message": "✅ PDF uploaded and processed!"}

@app.post("/ask/")
async def ask_question(query: str = Form(...)):
    """
    Ask a question related to the uploaded PDF.
    """
    if not vectorstore:
        return {"error": "⚠️ No PDF uploaded yet."}

    # Find similar chunks
    docs = vectorstore.similarity_search(query, k=5)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are an intelligent assistant. Use the following context to answer the question.

Context:
{context}

Question: {query}
Answer:"""

    try:
        # Use Gemini to generate the answer
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return {"response": response.text if hasattr(response, "text") else str(response)}
    except Exception as e:
        return {"error": str(e)}

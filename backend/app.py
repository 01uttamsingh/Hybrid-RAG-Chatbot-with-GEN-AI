from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pdf_loader import load_all_pdfs
from vector_store import build_vector_store, get_relevant_chunks
from gemini_client import ask_gemini_doc, ask_gemini_general
from config import SIMILARITY_THRESHOLD

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Build knowledge (run ONCE after putting PDFs)
@app.get("/build")
def build_knowledge():
    documents = load_all_pdfs()
    if not documents:
        return {"status": "No PDFs found"}

    build_vector_store(documents)
    return {"status": "Vector database built successfully"}


# ✅ Ask questions (HYBRID MODE)
@app.get("/ask")
def ask(question: str):
    try:
        result = get_relevant_chunks(question)
        
        # --- DEBUG LOGGING ---
        if result:
            print(f"Query: {question}")
            print(f"Found Score: {result['score']} (Threshold: {SIMILARITY_THRESHOLD})")
            print(f"Chunk Preview: {result['text'][:100]}...")
        else:
            print("No matching chunks found.")
        # ---------------------

        if result and result["score"] > SIMILARITY_THRESHOLD:
            print("✅ Status: USING PDF")
            answer = ask_gemini_doc(question, result["text"])
            source = "document"
            doc_name = result.get("meta", {}).get("doc_id") if "meta" in result else None
        else:
            print("⚠️ Status: USING GENERAL GEMINI (Score too low)")
            answer = ask_gemini_general(question)
            source = "general"
            doc_name = None

        return {
            "question": question,
            "source": source,
            "document": doc_name,
            "answer": answer
        }

    except Exception as e:
        print(f"SERVER ERROR: {e}")
        return {
            "error": "Internal Server Error in /ask",
            "details": str(e)
        }
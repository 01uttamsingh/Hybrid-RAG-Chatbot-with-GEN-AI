import os
import fitz
from typing import List, Dict
from config import PDF_FOLDER

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80) -> List[str]:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = max(0, end - overlap)

    return chunks


def load_all_pdfs() -> List[Dict]:
    documents = []

    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith(".pdf"):
            path = os.path.join(PDF_FOLDER, filename)
            full_text = extract_text_from_pdf(path)
            chunks = chunk_text(full_text)

            for idx, chunk in enumerate(chunks):
                documents.append({
                    "doc_id": filename,
                    "chunk_id": f"{filename}_chunk_{idx}",
                    "text": chunk
                })

    return documents

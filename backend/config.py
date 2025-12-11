import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_DIR = os.path.join(BASE_DIR, "..", "dataset")
PDF_FOLDER = os.path.join(DATASET_DIR, "uploaded_pdfs")
VECTOR_DB_PATH = os.path.join(DATASET_DIR, "vector_store")

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(VECTOR_DB_PATH, exist_ok=True)

SIMILARITY_THRESHOLD = 0.28

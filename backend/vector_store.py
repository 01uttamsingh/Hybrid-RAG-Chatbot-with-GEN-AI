import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import VECTOR_DB_PATH

model = SentenceTransformer("all-MiniLM-L6-v2")

index_path = os.path.join(VECTOR_DB_PATH, "faiss.index")
meta_path = os.path.join(VECTOR_DB_PATH, "metadata.npy")
text_path = os.path.join(VECTOR_DB_PATH, "texts.npy")

def build_vector_store(documents):
    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts)
    
    # ✅ FIX: Normalize embeddings for Cosine Similarity
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    
    # ✅ FIX: Use Inner Product (IP) instead of L2 Distance
    index = faiss.IndexFlatIP(dim) 
    index.add(embeddings)

    faiss.write_index(index, index_path)
    np.save(text_path, np.array(texts, dtype=object))
    np.save(meta_path, np.array(documents, dtype=object))

def get_relevant_chunks(question: str):
    if not os.path.exists(index_path):
        return None

    index = faiss.read_index(index_path)
    texts = np.load(text_path, allow_pickle=True)
    metadata = np.load(meta_path, allow_pickle=True)

    # ✅ FIX: Normalize query vector too
    query_embedding = model.encode([question])
    faiss.normalize_L2(query_embedding)
    
    scores, indices = index.search(query_embedding, 1)

    best_score = float(scores[0][0])
    best_idx = int(indices[0][0])

    return {
        "text": texts[best_idx],
        "score": best_score, # Now this is Cosine Similarity (0 to 1)
        "meta": metadata[best_idx]
    }
# modules/retriever.py
import numpy as np
from sentence_transformers import SentenceTransformer
from modules.embedder import get_faiss_index

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_questions(user_profile, top_k=5):
    index, id2question = get_faiss_index()
    query = " ".join(user_profile["skills"]) or user_profile["stream"]
    query_embedding = model.encode([query])
    scores, indices = index.search(np.array(query_embedding), top_k)
    return [id2question[i] for i in indices[0]]

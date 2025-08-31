# modules/embedder.py
import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index_file = "data/faiss_index/index.faiss"
mapping_file = "data/faiss_index/id2question.json"

def load_questions(stream):
    with open("data/questions.json", "r") as f:
        all_qs = json.load(f)
    return all_qs.get(stream, [])

def build_faiss_index(stream):
    questions = load_questions(stream)
    embeddings = model.encode(questions)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    
    os.makedirs("data/faiss_index", exist_ok=True)
    faiss.write_index(index, index_file)
    with open(mapping_file, "w") as f:
        json.dump(questions, f)

def get_faiss_index():
    index = faiss.read_index(index_file)
    with open(mapping_file, "r") as f:
        id2question = json.load(f)
    return index, id2question

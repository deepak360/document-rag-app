from sentence_transformers import SentenceTransformer
import numpy as np

# model = SentenceTransformer("all-MiniLM-L6-v2")#80 MB with 384 dimentions
model = SentenceTransformer("BAAI/bge-small-en-v1.5")#100MB but powerfull

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def generate_embeddings(text: str):
    chunks = chunk_text(text)
    embeddings = model.encode(chunks).tolist()  # list of vectors
    return chunks, embeddings

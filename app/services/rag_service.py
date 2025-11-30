from google import genai
import os
import numpy as np
from dotenv import load_dotenv
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def get_embeddings(texts):
    try:
        if not texts:
            print("No texts to embed")
            return []
        
        print(f"Generating embeddings for {len(texts)} chunks...")
        
        embeddings = []
        for i, text in enumerate(texts):
            try:
                result = client.models.embed_content(
                    model="text-embedding-004",
                    contents=text  # ← Changed from 'content' to 'contents'
                )
                embeddings.append(result.embeddings[0].values)
                print(f"✓ Generated embedding {i+1}/{len(texts)}")
                time.sleep(0.1)
            except Exception as e:
                print(f"✗ Error embedding chunk {i}: {e}")
                embeddings.append([0.0] * 768)
        
        print(f"Total embeddings generated: {len(embeddings)}")
        return embeddings
    except Exception as e:
        print(f"Embedding Error: {e}")
        return [[0.0] * 768 for _ in texts]

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    norm_product = np.linalg.norm(a) * np.linalg.norm(b)
    if norm_product == 0:
        return 0.0
    return np.dot(a, b) / norm_product

def retrieve_relevant_chunks(question, chunks, chunk_embeddings, top_k=3):
    try:
        if not chunks or not chunk_embeddings:
            return "No document content available."
        
        print(f"Retrieving relevant chunks for: '{question[:50]}...'")
        question_embedding = get_embeddings([question])[0]
        
        scores = []
        for i, chunk_emb in enumerate(chunk_embeddings):
            score = cosine_similarity(question_embedding, chunk_emb)
            scores.append((score, i))
        
        scores.sort(reverse=True)
        print(f"Top 3 chunk scores: {[f'{s:.3f}' for s, _ in scores[:3]]}")
        
        top_chunks = [chunks[idx] for _, idx in scores[:top_k]]
        return "\n\n".join(top_chunks)
    except Exception as e:
        print(f"Retrieval Error: {e}")
        return "\n\n".join(chunks[:3]) if chunks else "No content available."
import os
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="vector_db")
collection = client.get_collection("docs")

def embed_query(query: str):
    try:
        embedding = model.encode(query).tolist()
        return embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        return []

def semantic_search(query, top_k=3):
    print("Starting semantic search")
    try:
        query_vec = embed_query(query)
        print("Query embedded")
        results = collection.query(
            query_embeddings=[query_vec],
            n_results=top_k
        )
        print("ChromaDB query done")
        return results["documents"], results["metadatas"]
    except Exception as e:
        print(f"Semantic search error: {e}")
        return [], []

if __name__ == "__main__":
    docs, metas = semantic_search("knee surgery covered for 3 month policy in Pune?")
    for doc, meta in zip(docs[0], metas[0]):
        print(meta, doc)

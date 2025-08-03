import os
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="vector_db")
collection = client.get_collection("docs")

def embed_query(query: str):
    embedding = model.encode(query).tolist()
    return embedding

def semantic_search(query, top_k=5):
    query_vec = embed_query(query)
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=top_k
    )
    return results["documents"], results["metadatas"]

if __name__ == "__main__":
    docs, metas = semantic_search("knee surgery covered for 3 month policy in Pune?")
    for doc, meta in zip(docs[0], metas[0]):
        print(meta, doc)

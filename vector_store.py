import chromadb
import os, json

client = chromadb.PersistentClient(path="vector_db")
collection = client.get_or_create_collection("docs")

def load_embeddings(emb_folder="embeddings"):
    for fname in os.listdir(emb_folder):
        with open(os.path.join(emb_folder, fname), "r", encoding="utf-8") as f:
            data = json.load(f)
        collection.add(
            documents=[data["text"]],
            embeddings=[data["embedding"]],
            metadatas=[{"file": data["file"], "chunk_id": data["chunk_id"]}],
            ids=[f"{data['file']}_{data['chunk_id']}"]
        )
if __name__ == "__main__":
    load_embeddings()

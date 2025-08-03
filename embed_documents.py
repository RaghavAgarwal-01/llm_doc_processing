import os
import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    return model.encode(text).tolist()

def embed_chunks(input_folder="preprocessed", output_folder="embeddings"):
    os.makedirs(output_folder, exist_ok=True)
    files = os.listdir(input_folder)
    for fname in tqdm(files, desc="Embedding chunks"):
        fin = os.path.join(input_folder, fname)
        fout = os.path.join(output_folder, fname)
        if os.path.exists(fout):
            continue 
        with open(fin, "r", encoding="utf-8") as f:
            data = json.load(f)
        embedding = get_embedding(data["text"])
        data["embedding"] = embedding
        with open(fout, "w", encoding="utf-8") as g:
            json.dump(data, g, indent=2)

if __name__ == "__main__":
    embed_chunks()

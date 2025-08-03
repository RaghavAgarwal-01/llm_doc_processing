import json, re
from typing import List

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(text: str, chunk_size=500) -> List[str]:
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def preprocess_ocr_outputs(input_folder="ocr_outputs", output_folder="preprocessed"):
    import os
    os.makedirs(output_folder, exist_ok=True)
    for fname in os.listdir(input_folder):
        with open(os.path.join(input_folder, fname), "r", encoding="utf-8") as f:
            data = json.load(f)
        text = clean_text(data["text"])
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            out = {
                "file": data["path"],
                "chunk_id": idx,
                "text": chunk
            }
            with open(os.path.join(output_folder, f"{fname}_{idx}.json"), "w", encoding="utf-8") as outf:
                json.dump(out, outf, indent=2)

if __name__ == "__main__":
    preprocess_ocr_outputs()

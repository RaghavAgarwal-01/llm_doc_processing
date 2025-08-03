import os
from typing import List

def get_document_paths(folder: str = "documents") -> List[str]:
    files = []
    for root, _, filenames in os.walk(folder):
        for fname in filenames:
            if fname.lower().endswith((".pdf", ".docx", ".jpg", ".png")):
                files.append(os.path.join(root, fname))
    return files

if __name__ == "__main__":
    docs = get_document_paths()
    print("Found files:", docs)

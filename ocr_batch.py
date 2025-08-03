from ingest import get_document_paths
from ocr_client import ocr_parse, get_parsed_text
import os, json
from tqdm import tqdm

def batch_ocr(doc_folder="documents", output_folder="ocr_outputs"):
    os.makedirs(output_folder, exist_ok=True)
    docs = get_document_paths(doc_folder)
    for doc in tqdm(docs):
        fname = os.path.basename(doc)
        out_path = os.path.join(output_folder, fname + ".json")
        if os.path.exists(out_path): continue  # skip already done
        ocr_json = ocr_parse(doc)
        result = {
            "path": doc,
            "text": get_parsed_text(ocr_json)
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

if __name__ == "__main__":
    batch_ocr()

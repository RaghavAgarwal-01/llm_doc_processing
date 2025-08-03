# LLM Document Processing System

An end-to-end LLM-powered pipeline for intelligent query processing, semantic retrieval, and decision automation on large, unstructured insurance and policy documents.

---

## Features

- **Document Ingestion:** Supports PDFs, images (JPEG/PNG), and Word documents.
- **OCR Extraction:** Uses the free OCR.Space API to convert scanned/digital documents into text.
- **Text Processing:** Cleans and chunks documents into manageable pieces.
- **Semantic Embeddings:** Employs the open-source SentenceTransformers model (`all-MiniLM-L6-v2`) for local and free vector embeddings.
- **Vector Storage & Retrieval:** Saves embeddings in ChromaDB for semantic search and similarity queries.
- **Decision Engine:** Uses a local LLM (e.g., Ollama with Llama 2, Mistral) or rule-based logic to interpret relevant clauses and generate structured decisions with justifications.
- **REST API:** Provides a Flask API endpoint for natural language queries returning structured JSON responses with decisions, amounts, and clause-level justification.

---

## Project Structure
```
llm_doc_processing/
│
├── api_server.py
├── config.py
├── ingest.py
├── ocr_client.py
├── ocr_batch.py
├── preprocess.py
├── embed_documents.py
├── vector_store.py
├── semantic_search.py
├── decision_engine.py
├── requirements.txt
└── README.md

```
## Setup Instructions

1. **Clone the repository and create a virtual environment:**
    ```
    git clone https://github.com/yourusername/llm_doc_processing.git
    cd llm_doc_processing
    python -m venv .venv
    source .venv/bin/activate            # Mac/Linux
    .\.venv\Scripts\activate             # Windows
    ```

2. **Install dependencies:**
    ```
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

3. **Configure API Keys:**
    - Open `config.py` and set your free OCR.Space API key (`OCR_API_KEY`).
    - Ensure your local LLM server (e.g., Ollama) is running if using LLM decision engine.

4. **Add Documents:**
    - Place PDFs, DOCXs, and image files in a folder named `documents/`.

---

## Running the Pipeline

Run the following scripts in order:

1. **Extract OCR text:**
    ```
    python ocr_batch.py
    ```

2. **Preprocess and chunk text:**
    ```
    python preprocess.py
    ```

3. **Embed chunks into vectors locally:**
    ```
    python embed_documents.py
    ```

4. **Load embeddings into vector database:**
    ```
    python vector_store.py
    ```

5. **Start the Flask API server:**
    ```
    python api_server.py
    ```

The API will be available at `http://localhost:5000`.

---

## Querying the API

Use tools like Postman or curl to send POST requests:

curl -X POST "http://localhost:5000/ask"
-H "Content-Type: application/json"
-d '{"query": "32-year-old female, cataract surgery in Mumbai, policy active for 18 months"}'


---

## Local LLM Setup (Optional)

- Install [Ollama](https://ollama.com/) to run local LLMs like Llama 2 or Mistral.
- Run your chosen model:

ollama run llama2


Your decision engine will communicate with this local server to generate responses.

---

## Notes

- Supports basic document formats; for additional formats like emails or Excel, extend `ingest.py`.
- You can customize prompts and processing in `decision_engine.py`.
- Ensure your API keys remain private and secure.
- The project can be expanded with UI, more complex policy handling, and additional document types.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributions & Support

Feel free to fork, raise issues, or submit pull requests. For help or questions, open an issue in this repository.

---

**Happy hacking and good luck with your project!**

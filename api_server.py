from flask import Flask, request, jsonify
from functools import lru_cache
import os

app = Flask(__name__)

from semantic_search import semantic_search
from decision_engine import decide, parse_model_response


@lru_cache(maxsize=128)
def cached_process(query):
    docs, _ = semantic_search(query) 
    return decide(query, docs)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True, silent=True)
    if not data or "query" not in data or not isinstance(data.get("query"), str) or not data.get("query").strip():
        return jsonify({
            "Decision": "rejected",
            "Amount": 0,
            "Justification": [],
            "Note": "Invalid or missing 'query' parameter."
        }), 400

    query = data.get("query").strip()
    print(f"Received query: {query}")

    try:
        raw_response = cached_process(query)
        print(f"Raw response from decide(): {raw_response}")
        structured = parse_model_response(raw_response)
    except Exception as e:
        print(f"Error during processing: {e}")
        structured = {
            "Decision": "rejected",
            "Amount": 0,
            "Justification": [],
            "Note": "Internal processing error."
        }

    if not structured or "Decision" not in structured:
        structured = {
            "Decision": "rejected",
            "Amount": 0,
            "Justification": [],
            "Note": "Failed to parse model response."
        }

    print(f"Returning response: {structured}")
    return jsonify(structured)


def warmup():
    print("Warming up LLM...")
    _ = decide("warmup", ["Warmup clause."])
    print("Warmup complete.")

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        warmup()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
else:
    warmup()

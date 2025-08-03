from flask import Flask, request, jsonify
from decision_engine import decide
from semantic_search import semantic_search
import json
import re
def parse_model_response(response_text: str):
    def flatten_justification(justification):
        flat_list = []
        for item in justification:
            if isinstance(item, list):
                flat_list.extend(item)
            else:
                flat_list.append(item)
        return flat_list

    json_match = re.search(r'{.*?}', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        try:
            parsed = json.loads(json_str)
            parsed.setdefault("Decision", "rejected")
            if "Amount" not in parsed or not isinstance(parsed["Amount"], (int, float)):
                parsed["Amount"] = 0
            if "Justification" not in parsed or not isinstance(parsed["Justification"], list):
                parsed["Justification"] = []
            else:
                parsed["Justification"] = flatten_justification(parsed["Justification"])
            return parsed
        except json.JSONDecodeError:
            pass
    return {
        "Decision": "rejected",
        "Amount": 0,
        "Justification": [],
        "Note": "Could not parse model response cleanly."
    }

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    docs, _ = semantic_search(query)
    raw_result = decide(query, docs[0])
    raw_text = raw_result if isinstance(raw_result, str) else json.dumps(raw_result)
    structured_result = parse_model_response(raw_text)
    return jsonify(structured_result)

if __name__ == "__main__":
    app.run(port=5000)

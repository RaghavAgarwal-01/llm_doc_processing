import json
import re
import requests


def decide(query, docs):
    """
    Calls an LLM (e.g., local Ollama instance) with a prompt and returns the raw text decision response.
    - query: the user query
    - docs: a list of relevant document text chunks (from semantic_search)
    """
    prompt = (
        f"Given these insurance clauses:\n{docs}\n\n"
        f"And the query:\n{query}\n"
        'Answer ONLY in JSON as { "Decision": "approved/denied", "Amount": <integer>, "Justification": [clauses used] }.'
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt},
        stream=True
    )

    full_response_text = ""
    for line in response.iter_lines():
        if line:
            try:
                json_line = json.loads(line.decode("utf-8"))
                full_response_text += json_line.get("response", "")
                if json_line.get("done", False):
                    break
            except Exception:
                continue

    return full_response_text

def parse_model_response(response_text: str):
    """
    Parses the raw LLM response text to extract a clean JSON object with keys:
    Decision (str), Amount (int/float), Justification (list of strings).
    Flattens nested lists in Justification if needed.
    """
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
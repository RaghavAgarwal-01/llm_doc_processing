import json
import requests

def decide(query, docs):
    """
    Sends the prompt to the LLM server and returns the full JSON string response.
    Properly handles streaming chunks by extracting and concatenating only the `response` fields.
    """
    prompt = (
        f"Given these insurance clauses:\n{docs}\n\n"
        f"AND the query:\n{query}\n\n"
        "Answer ONLY with a SINGLE valid JSON object in exactly this format:\n"
        "{\n"
        '  "Decision": "approved" or "denied",\n'
        '  "Amount": <integer>,\n'
        '  "Justification": [list of clauses used]\n'
        "}\n"
        "Do NOT include any additional explanations or text."
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "max_new_tokens": 128,
                "temperature": 0.0,
                "stop": ["}"],
            },
            stream=True,
            timeout=60
        )
    except requests.exceptions.RequestException as e:
        print(f"LLM request error: {e}")
        # Return JSON string fallback so that parse_model_response can parse it
        return json.dumps({
            "Decision": "rejected",
            "Amount": 0,
            "Justification": ["LLM request failed"]
        })

    full_response_text = ""
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            try:
                decoded = chunk.decode("utf-8")
                # The streaming API sends line-delimited JSON objects.
                for line in decoded.splitlines():
                    if not line.strip():
                        continue
                    try:
                        obj = json.loads(line)
                        if "response" in obj and obj["response"]:
                            full_response_text += obj["response"]
                    except json.JSONDecodeError:
                        # Ignore partial/not well-formed JSON lines in chunks
                        pass
            except Exception as e:
                print(f"Error decoding chunk: {e}")

    return full_response_text

def parse_model_response(response_text: str):
    """
    Parses the raw LLM response text to extract a single well-formed JSON object.
    Flattens nested justification lists for consistent output.
    Returns fallback dict if parse fails.
    """
    def flatten_justification(justification):
        flat_list = []
        for item in justification:
            if isinstance(item, list):
                flat_list.extend(item)
            else:
                flat_list.append(item)
        return flat_list

    start = None
    brace_count = 0
    for i, c in enumerate(response_text):
        if c == '{':
            if start is None:
                start = i
            brace_count += 1
        elif c == '}':
            brace_count -= 1
            if brace_count == 0 and start is not None:
                json_str = response_text[start: i+1]
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
                    # Continue to search for next potential JSON object
                    pass

    # Fallback if parsing fails
    return {
        "Decision": "rejected",
        "Amount": 0,
        "Justification": [],
        "Note": "Could not parse model response cleanly."
    }
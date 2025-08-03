import requests
from config import OCR_API_KEY, OCR_ENDPOINT

def ocr_parse(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            OCR_ENDPOINT,
            files={"file": f},
            data={"language": "eng", "isOverlayRequired": "false"},
            headers={"apikey": OCR_API_KEY}
        )
    result = response.json()
    return result

def get_parsed_text(ocr_json):
    try:
        return ocr_json["ParsedResults"][0]["ParsedText"]
    except (KeyError, IndexError):
        return ""

if __name__ == "__main__":
    j = ocr_parse("sample.pdf")
    print(get_parsed_text(j))

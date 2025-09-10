import re
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL=os.getenv('ALTSCORE_BASE_URL')
S1_E7_SOLUTION_PATH="v1/s1/e7/solution"

# TODO: This URL has to be updated because it will change each time that 
#       the container are stoped (docker-compose down) and rerunned (docker-compose up).
#       visit the url http://localhost:4040
NGROK_APP_URL = "https://a57d2f54bbff.ngrok-free.app"

def main(key: str):

    # 1) Sanity-check live endpoints before submitting
    expected_html = """<!DOCTYPE html>
<html>
<head>
    <title>Repair</title>
</head>
<body>
<div class=\"anchor-point\">ENG-04</div>
</body>
</html>"""

    # GET /status
    r = requests.get(f"{NGROK_APP_URL}/status", timeout=5)
    assert r.status_code == 200, f"/status code={r.status_code} body={r.text}"
    j = r.json()
    assert j.get("damaged_system") == "engines", f"/status payload unexpected: {j}"

    # GET /repair-bay
    r = requests.get(f"{NGROK_APP_URL}/repair-bay", timeout=5)
    assert r.status_code == 200, f"/repair-bay code={r.status_code}"
    assert r.text.strip() == expected_html.strip(), "repair-bay HTML mismatch"

    # POST /teapot
    r = requests.post(f"{NGROK_APP_URL}/teapot", timeout=5)
    assert r.status_code == 418, f"/teapot code={r.status_code} body={r.text}"
    assert r.json().get("detail") == "I'm a teapot", f"/teapot payload unexpected: {r.text}"

    # GET /healthz
    r = requests.get(f"{NGROK_APP_URL}/healthz", timeout=5)
    assert r.status_code == 200 and r.json().get("status") == "ok", "/healthz failed"

    headers = {
        'API-KEY': key,
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    payload = {
        "base_url": NGROK_APP_URL
    }

    r = requests.post(
        f"{BASE_URL}/{S1_E7_SOLUTION_PATH}",
        headers=headers,
        json=payload,
        timeout=30,
    )

    detail = r.text
    print(detail)
    r.raise_for_status()

    print(r.json())


if __name__ == "__main__":
    # Get API key from environment variables
    key = os.getenv('ALTSCORE_API_KEY')
    if not key:
        raise ValueError("ALTSCORE_API_KEY not found in environment variables. Please check your .env file.")

    main(key=key)

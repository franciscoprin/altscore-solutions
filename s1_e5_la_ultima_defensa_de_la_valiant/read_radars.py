import re
import requests
import time
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL=os.getenv('ALTSCORE_BASE_URL')
S1_E5_SOLUTION_PATH="v1/s1/e5/actions/perform-turn"


def main(key: str):

    headers = {
        'API-KEY': key,
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    payload = {
        "action": "radar",
        "attack_position": None,
    }

    r = requests.post(
        f"{BASE_URL}/{S1_E5_SOLUTION_PATH}",
        headers=headers,
        json=payload,
        timeout=30,
    )

    detail = r.text
    print(detail)

    # Append raw response text to a log file with a timestamp
    try:
        with open("radars_responses.log", "a", encoding="utf-8") as f:
            f.write(f"--- {time.strftime('%Y-%m-%d %H:%M:%S')} RAW ---\n")
            f.write(detail)
            f.write("\n")
    except Exception as e:
        print(f"[warn] failed to write raw response to log: {e}")

    r.raise_for_status()

    data = r.json()
    print(data)

    # Append parsed JSON response as pretty JSON
    try:
        with open("radars_responses.log", "a", encoding="utf-8") as f:
            f.write(f"--- {time.strftime('%Y-%m-%d %H:%M:%S')} JSON ---\n")
            f.write(json.dumps(data, ensure_ascii=False, indent=2))
            f.write("\n")
    except Exception as e:
        print(f"[warn] failed to write JSON response to log: {e}")


if __name__ == "__main__":
    key = os.getenv('ALTSCORE_API_KEY')
    if not key:
        raise ValueError("ALTSCORE_API_KEY not found in environment variables. Please check your .env file.")

    main(key=key)

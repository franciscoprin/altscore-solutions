import re
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL=os.getenv('ALTSCORE_BASE_URL')
S1_E7_SOLUTION_PATH="/v1/s1/e5/actions/perform-turn"


def main(key: str):

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # TODO: REPLACE THESE TWO!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    X = "c"
    Y = 7

    headers = {
        'API-KEY': key,
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    payload = {
        "action": "attack",
        "attack_position": {
            "x": X,
            "y": Y,
        },
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
    key = os.getenv('ALTSCORE_API_KEY')
    if not key:
        raise ValueError("ALTSCORE_API_KEY not found in environment variables. Please check your .env file.")

    main(key=key)

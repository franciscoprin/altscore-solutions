import re
import requests
import base64
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()

# Configuration
BASE_URL=os.getenv('ALTSCORE_BASE_URL')
S1_E4_SOLUTION_PATH="v1/s1/e4/solution"


def main(key: str):
    payload = {
        "username": "Not all those who wander",
        "password": "are lost",
    }

    headers = {
        'API-KEY': key,
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    r = requests.post(
        f"{BASE_URL}/{S1_E4_SOLUTION_PATH}",
        headers=headers,
        json=payload,
        timeout=10,
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

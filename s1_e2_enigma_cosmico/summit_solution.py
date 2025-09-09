import re
import requests
import time
from dotenv import load_dotenv
from typing import Any, Iterator

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv('ALTSCORE_BASE_URL')

S1_E2_API_PATH = "v1/s1/e2/resources/stars"
S1_E2_SOLUTION_PATH = "v1/s1/e2/solution"

def start_generator(key: str) -> Iterator[dict[str, Any]]:
    headers = {
        'API-KEY': key,
        'accept': 'application/json',
    }

    page = 0
    stars = [1]

    while len(stars) > 0:
        page += 1
        params = {
            "page": page,
            "sort-by": "resonance",
            "sort-direction": "desc",
        }

        r = requests.get(
            f"{BASE_URL}/{S1_E2_API_PATH}",
            headers=headers,
            params=params,
            timeout=10,
        )
        detail = r.text
        print(detail)
        r.raise_for_status()
        stars = r.json()
    
        yield from stars

def main(key: str):
    total_resonance = 0
    total_starts = 0
    for start in start_generator(key=key):
        total_resonance += start['resonance']
        total_starts += 1

    headers = {
        'API-KEY': key,
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    payload = {"average_resonance": int(total_resonance / total_starts)}

    print(payload)


    r = requests.post(
        f"{BASE_URL}/{S1_E2_SOLUTION_PATH}",
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


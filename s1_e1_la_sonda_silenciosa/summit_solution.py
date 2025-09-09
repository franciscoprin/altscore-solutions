import re
import requests
import time
import os
from dotenv import load_dotenv
from register import register, RegisterRequest

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv('ALTSCORE_BASE_URL')
S1_E1_API_PATH = "v1/s1/e1/resources/measurement"
S1_E1_SOLUTION_PATH = "v1/s1/e1/solution"

def main(key: str):
    velocity = None
    headers = {
        'API-KEY': key
    }
    while True:
        r = requests.get(
            f"{BASE_URL}/{S1_E1_API_PATH}",
            headers=headers,
            timeout=15,
        )

        r.raise_for_status()

        m = r.json()

        print("distance: ", m["distance"])
        print("time: ", m["time"])

        # Match integers or decimals (e.g., "862" or "2.128395061728395")
        distance = re.findall(r'\d+(?:\.\d+)?', m["distance"])
        sonda_time = re.findall(r'\d+(?:\.\d+)?', m["time"])

        if len(distance) > 0 and len(sonda_time) > 0:
            velocity = int(float(distance[0]) / float(sonda_time[0]))
            break

        print("Trying...")
        time.sleep(3)

    payload = {"speed": velocity}

    print(payload)

    r = requests.post(
        f"{BASE_URL}/{S1_E1_SOLUTION_PATH}",
        headers=headers,
        json=payload,
        timeout=15,
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

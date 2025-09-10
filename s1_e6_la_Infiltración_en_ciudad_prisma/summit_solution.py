import re
import requests
import time
from register import register, RegisterRequest
from typing import Any, Iterator
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()

# Configuration
BASE_URL=os.getenv('ALTSCORE_BASE_URL')
REGISTER_PATH="v1/register"

S1_E6_SOLUTION_PATH="v1/s1/e6/solution"

POKENMON_BASE_URL="https://pokeapi.co/api/v2/pokemon"

def pokemon_generator() -> Iterator[dict[str, Any]]:
    # Paginate over all Pokémon from PokeAPI using 'next' links.
    # key is unused here but kept for signature compatibility.
    url = f"{POKENMON_BASE_URL}?limit=200&offset=0&order_by=name"
    while url:
        r = requests.get(url, timeout=15)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            # Print server-provided detail for debugging
            print(r.text)
            raise

        data = r.json()
        results = data.get("results", [])
        for pokemon in results:
            # Each item is typically: {"name": "bulbasaur", "url": ".../pokemon/1/"}
            yield pokemon
        
        time.sleep(3)

        url = data.get("next")

from pprint import pprint

def main(key: str):
    start_time = time.time()
    total_height = defaultdict(lambda: defaultdict(int))

    for p in pokemon_generator():
        detail = requests.get(p["url"], timeout=15)
        detail.raise_for_status()

        info = detail.json()
        name = info["name"]
        height = info["height"]

        for p_type_info in info["types"]:
            total_height[p_type_info["type"]["name"]]["height"] += height
            total_height[p_type_info["type"]["name"]]["count"] += 1

    height = dict()
    for p_type in sorted(total_height.keys()):
        height[p_type] = round(total_height[p_type]["height"] / total_height[p_type]["count"], 3)

    headers = {
        'API-KEY': key,
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    payload = {"heights": height}
    print(payload)


    r = requests.post(
        f"{BASE_URL}/{S1_E6_SOLUTION_PATH}",
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


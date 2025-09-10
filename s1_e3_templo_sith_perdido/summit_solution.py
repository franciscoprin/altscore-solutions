import re
import requests
import base64
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()

# Configuration
BASE_URL=os.getenv('ALTSCORE_BASE_URL')

S1_E3_API_PATH="v1/s1/e3/resources/oracle-rolodex"
S1_E3_SOLUTION_PATH="v1/s1/e3/solution"

# Note: SWAPI SSL Workaround
# The official SWAPI (https://swapi.dev/) has SSL certificate issues.
# As a workaround, use this local instance:
# 1. Clone the forked repo: https://github.com/franciscoprin/swapi
# 2. Run: docker-compose up
# This will start a local SWAPI instance at http://localhost:8001
STAR_WARS_PEOPLE_URL="http://localhost:8001/api/people"


def main(key: str):
    headers = {
        'API-KEY': key,
        'accept': 'application/json',
    }
    
    planets = defaultdict(lambda: defaultdict(int))

    next_page = f"{STAR_WARS_PEOPLE_URL}?page=1"
    while next_page is not None:
        r = requests.get(next_page)
        r.raise_for_status()
        response = r.json()

        people = response["results"]
        next_page = response["next"]

        for person in people:
            r = requests.get(
                f"{BASE_URL}/{S1_E3_API_PATH}",
                headers=headers,
                params={
                    "name": person['name'],
                }
            )
            
            r.raise_for_status()
            oracle_notes = base64.b64decode(r.json()['oracle_notes']).decode('utf-8')
            homeworld = person['homeworld']

            if "Light Side" in oracle_notes:
                planets[homeworld]['light_side'] += 1

            if "Dark Side" in oracle_notes:
                planets[homeworld]['dark_side'] += 1

            planets[homeworld]['total'] += 1

    balance_planet = None
    for planet, force_info in planets.items():
        if force_info.get('light_side', 0) == force_info.get('dark_side', 0):
            balance_planet = planet

    r = requests.get(balance_planet)
    detail = r.text
    print(detail)
    r.raise_for_status()
    response = r.json()

    print("balance_planet: ", response["name"])
    
    payload = {"planet": response["name"]}
    headers = {
        'API-KEY': key,
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    print(payload)

    r = requests.post(
        f"{BASE_URL}/{S1_E3_SOLUTION_PATH}",
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

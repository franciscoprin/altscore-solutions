# S1E6 - La Infiltración en Ciudad Prisma: Un Desafío para los Maestros de Datos 🏙️

[View Challenge](https://makers-challenge.altscore.ai/s1e6)

## The Challenge
In a remote corner of the Pokémon world, Prisma City has remained closed to trainers and Pokémon for decades. To gain access, you must demonstrate your mastery of Pokémon data handling by solving the guardians' challenge.

### Your Mission
Calculate the average height of all Pokémon types, in alphabetical order, with a precision of 3 decimal places.

## The Solution
The solution involves querying the PokeAPI to obtain data for all Pokémon, processing their heights by type, and calculating the required averages.

### Implementation
The `summit_solution.py` script performs the following actions:
1. Queries the PokeAPI to retrieve all Pokémon
2. Collects the heights and types of each Pokémon
3. Calculates the average height by type
4. Sends the results to the solution endpoint

### Solution Code
```python
# Simplified code - see summit_solution.py for the complete implementation
import requests
from collections import defaultdict

def calculate_average_heights():
    # Query all Pokémon
    url = "https://pokeapi.co/api/v2/pokemon"
    all_pokemon = []
    
    # Paginate through all Pokémon
    while url:
        response = requests.get(url)
        data = response.json()
        all_pokemon.extend(data['results'])
        url = data['next']
    
    # Process heights by type
    type_heights = defaultdict(list)
    for pokemon in all_pokemon:
        details = requests.get(pokemon['url']).json()
        for type_info in details['types']:
            type_name = type_info['type']['name']
            type_heights[type_name].append(details['height'])
    
    # Calculate averages
    avg_heights = {}
    for type_name, heights in sorted(type_heights.items()):
        avg_heights[type_name] = round(sum(heights) / len(heights), 3)
    
    return avg_heights
```

### Results
The average heights by type are:

```json
{
    "heights": {
        "bug": 19.529,
        "dark": 20.064,
        "dragon": 43.374,
        "electric": 16.491,
        "fairy": 19.41,
        "fighting": 22.6,
        "fire": 28.99,
        "flying": 16.597,
        "ghost": 14.728,
        "grass": 16.822,
        "ground": 19.323,
        "ice": 18.273,
        "normal": 15.665,
        "poison": 33.706,
        "psychic": 16.206,
        "rock": 18.02,
        "steel": 27.758,
        "water": 22.758
    }
}
```

### Execution
```bash
python summit_solution.py
```

## Resources
- [PokeAPI](https://pokeapi.co/)
- [Challenge API Documentation](https://makers-challenge.altscore.ai/docs)

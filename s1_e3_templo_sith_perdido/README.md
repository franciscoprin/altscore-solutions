# S1E3 - La Búsqueda del Templo Sith Perdido 🏰

[View Challenge](https://makers-challenge.altscore.ai/s1e3)

## Solution Overview
This script helps locate a lost Sith temple by analyzing the balance of the Force across different planets in the Star Wars universe. The challenge involves processing character data from SWAPI and determining Force alignment through an Oracle's encoded messages.

### Key Features
- Processes Star Wars character data to determine Force alignment
- Calculates the Force Balance Index (IBF) for each planet
- Identifies the planet with perfect balance between Light and Dark sides
- Handles API communication with both SWAPI and the Oracle's endpoint

## Usage
Run the following command:
```bash
python summit_solution.py
```

### Expected Output
- List of stars with their resonance values and coordinates
- Calculated average resonance
- Success/failure status of the solution submission

## Implementation Notes
- Uses SWAPI (Star Wars API) to fetch character and planet data
- Queries the Oracle's endpoint to determine Force alignment for each character
- Calculates the Force Balance Index (IBF) for each planet
- Identifies the planet where Light and Dark sides are in perfect balance (IBF = 0)

### SWAPI Setup
Due to SSL certificate issues with the official SWAPI (see [original issue](https://github.com/phalt/swapi/issues/149)), this solution uses a local instance:
1. A forked version with Docker support is available at [franciscoprin/swapi](https://github.com/franciscoprin/swapi)
2. Run `docker-compose up` to start the local SWAPI instance at `http://localhost:8001`

### Oracle's Endpoint
The Oracle provides Force alignment information through encoded messages. Example responses:
```
Luke Skywalker:1:Luke Skywalker is a Jedi, and belongs to the Light Side of the Force.
Darth Vader:1:Darth Vader was once a Jedi but fell to the Dark Side; he belongs to the Dark Side.
```

The solution parses these messages to count Light Side and Dark Side users per planet.

### Force Balance Index (IBF)
For each planet, the script calculates:
```
IBF = (Light Side Users - Dark Side Users) / Total Users
```
A planet with perfect balance (IBF = 0) is the location of the lost Sith temple.

## Example Output

When you run the script, it will output the planet that's in perfect balance between the Light and Dark sides of the Force:

```bash
$ python summit_solution.py
{"name":"Ryloth","rotation_period":"30","orbital_period":"305",...}
balance_planet: Ryloth
{'planet': 'Ryloth'}
{"result":"correct"}
{'result': 'correct'}
```

This indicates that Ryloth is the planet with an equal number of Light Side and Dark Side Force users, making it the location of the lost Sith temple.

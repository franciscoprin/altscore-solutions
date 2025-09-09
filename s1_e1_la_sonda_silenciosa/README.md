# S1E1 - ¡La Sonda Silenciosa! 🛰️

[View Challenge](https://makers-challenge.altscore.ai/s1e1)

## Solution Overview
This script calculates the instantaneous orbital speed of a planet using data from a space probe. Due to cosmic interference, the probe's readings are not always reliable, so the script implements retry logic to handle failed attempts.

### Key Features
- Automatically retries failed measurements due to space interference
- Calculates speed using the formula: `speed = distance / time`
- Rounds the result to the nearest integer
- Handles API communication and error cases

## Usage
Run the following command:
```bash
python summit_solution.py
```

### Expected Output
- Distance (in astronomical units) and time (in hours) from the probe
- Calculated speed (distance / time)
- Success/failure status of the solution submission

## Implementation Notes
- The script handles intermittent probe responses by retrying until valid data is received
- Speed is calculated as `distance / time` and rounded to the nearest integer
- API key is loaded from environment variables (see main README for setup)

## Example Output

These are the sample output after running the script:

```bash
(venv) fprin@francisco-prin:~/personal/altscore/altscore-solutions/s1_e1_la_sonda_silenciosa$ python summit_solution.py

Trying...
distance:  failed to measure, try again
time:  failed to measure, try again
Trying...
distance:  failed to measure, try again
time:  failed to measure, try again

.... After numerous retries

Trying...
distance:  failed to measure, try again
time:  failed to measure, try again
Trying...
distance:  failed to measure, try again
time:  failed to measure, try again
Trying...
distance:  787 AU
time:  1.94320987654321 hours
{'speed': 405}
{"result":"correct"}
{'result': 'correct'}
```

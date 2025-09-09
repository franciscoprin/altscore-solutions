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

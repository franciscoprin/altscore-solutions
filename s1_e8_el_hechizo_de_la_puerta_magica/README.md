# S1E8 - El Hechizo de la Puerta Mágica 🚪

## Context
In the vast library of Altwarts, the ancient founders hid arcane knowledge, protected by a powerful spell known as "The Enchantment of the Magic Door". To unravel this knowledge, you must solve the riddle they left behind. Each clue will bring you closer to the final solution, but beware, for only the most astute wizards will be able to find the way.

## Clues

### First Clue: The Clock of Seconds
In the Clock Tower of Altwarts, time is both your greatest ally and your worst enemy. Each second marks the passage of a key that opens a door. Choose the right moment, and the key will be yours. But remember, only in the first second can you find the key to the first door.

### Second Clue: Action and Reaction, Doors Bring Revelation
In the Charms classroom, Professor Flitwick keeps an ancient scroll that speaks of hidden words, not in the spells themselves, but in the consequences of their casting. Each magical action generates a reaction, and within that reaction lie the secrets sought by astute wizards.

### Third Clue:
In the Great Hall, N magical doors are aligned, each unlocked by a single word. A misspoken spell will lose you, but the correct one will guide you. Only by advancing in order and at the right moment will you reach your goal.

### Fourth Clue:
Each door will lead you to the next, but the answer is not found at the end—the path itself is the key. Remember to use the `Revelio` spell to see what is hidden.

## Solution

### How It Works
The `read_messagues.py` script interacts with the Altwarts API to solve the Magic Door riddle. The process is as follows:

1. **Challenge Start**:
   - The server responds with a welcome message:
     ```
     {"response":"Welcome to the Altwarts challenge! You're in luck, here's the first clue."}
     ```

2. **Progress Through the Doors**:
   - Each API request returns a `gryffindor` cookie containing a base64-encoded message
   - These messages are individual words from a larger message
   - The server responds with messages like:
     ```
     {"response":"Correct, but you still have a way to go."}
     ```

3. **Challenge Completion**:
   - When the journey is complete, the server responds:
     ```
     {"response":"You have reached the end. Remember to use the 'revelio' spell to discover the hidden message."}
     ```

### Hidden Message
By decoding all the `gryffindor` cookies (which are in base64) and combining them, the hidden message is revealed:

```
Altwarts reveals how magic arises through perseverance, precision, and dedication when facing challenges. Every detail matters; true skill is reflected in the dedication to continuously improve.
```

### Usage
1. Make sure the `ALTSCORE_API_KEY` environment variable is set
2. Run the script:
   ```bash
   python read_messagues.py
   ```
3. The script will make the necessary requests and save progress to `door_probe_simple.log`

## Resources
- API to attempt opening a door: [POST] /v1/s1/e8/actions/door
- Submit your answer here: [POST] /v1/s1/e8/solution

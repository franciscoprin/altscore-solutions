# Altscore Solutions

## Setup Instructions

1. **Set Up a Virtual Environment (Recommended)**
   ```bash
   # Create a virtual environment
   python3 -m venv venv
   
   # Activate the virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and configure the following variables:
     - `ALTSCORE_ALIAS`: Your username (will be displayed on the leaderboard)
     - `ALTSCORE_COUNTRY`: Your country code in ISO3 format (e.g., 'MEX' for Mexico, 'ESP' for Spain, 'USA' for United States, 'COL' for Colombia, 'ARG' for Argentina)
     - `ALTSCORE_EMAIL`: Your email address where the AltScore API key will be sent
     - `ALTSCORE_APPLY_ROLE`: Your role - must be one of: 'engineering', 'data', or 'integrations'

3. **Get Your API Key**
   After configuring the `.env` file, run the register script:
   ```bash
   python register.py
   ```
   This will register your details and send an API key to the email address you specified in `ALTSCORE_EMAIL`.

4. **Update .env with Your API Key**
   - Check your email for the API key from AltScore
   - Open your `.env` file
   - Update the `ALTSCORE_API_KEY` variable with the key from your email

5. **Run the Solutions**
   You can now run the individual solution files, and they will automatically use the API key from your .env file.

## Security Note
- Never commit your `.env` file to version control
- The `.gitignore` file is already set up to exclude `.env`
- Keep your API key secure and don't share it publicly

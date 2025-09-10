import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

key = os.getenv('ALTSCORE_API_KEY')
if not key:
    raise ValueError("ALTSCORE_API_KEY not found in environment variables. Please check your .env file.")

url = "https://makers-challenge.altscore.ai/v1/s1/e8/solution"
headers = {
    "API-KEY": key,
    "Accept": "application/json",
    "Content-Type": "application/json"
}
payload = {"hidden_message": "Altwarts revela cómo la magia surge mediante perseverancia, precisión y esmero al enfrentar desafíos. Cada detalle importa; auténtica destreza se refleja con dedicación para mejorar continuamente"}
r = requests.post(url, headers=headers, json=payload, timeout=20)
print(r.status_code, r.text)

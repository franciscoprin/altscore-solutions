import requests

# Done!!!!
url = "https://makers-challenge.altscore.ai/v1/s1/e8/solution"
headers = {"API-KEY": "905cf7df9ad849138f4c26432ebb08b3", "Accept": "application/json", "Content-Type": "application/json"}
payload = {"hidden_message": "Altwarts revela cómo la magia surge mediante perseverancia, precisión y esmero al enfrentar desafíos. Cada detalle importa; auténtica destreza se refleja con dedicación para mejorar continuamente"}
r = requests.post(url, headers=headers, json=payload, timeout=20)
print(r.status_code, r.text)

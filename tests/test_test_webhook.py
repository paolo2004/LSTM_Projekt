import requests

url = "http://localhost:8080/webhook"

data = {"price": 123.45}

response = requests.post(url, json=data)

print("Response:", response.json())

import requests
import json

API_URL = "http://localhost:8000/api/calificaciones/"
AUTH_TOKEN = "Token 31d1ad7668c1285b8e46f7c197905ef709b0caf4"  # reemplazar con token real

headers = {
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json"
}

# Cambia aquí el nombre del archivo JSON correspondiente al usuario
filename = "json_data/user_5.json"

with open(filename, "r", encoding="utf-8") as file:
    data = json.load(file)

for entry in data:
    response = requests.post(API_URL, json=entry, headers=headers)
    if response.status_code == 201:
        print(f"✅ Calificación creada: Libro {entry['libro']} por Usuario {entry['user']} (score={entry['score']})")
    else:
        print(f"❌ Error con libro {entry['libro']} y usuario {entry['user']}")
        print("Detalles:", response.status_code, response.text)

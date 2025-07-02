import requests
import random
from datetime import datetime

API_URL = "http://localhost:8000/api/libros/"
AUTH_TOKEN = "Token 31d1ad7668c1285b8e46f7c197905ef709b0caf4"

headers = {
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json"
}

generos = [3, 5, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
calificaciones = [1, 2, 3, 4, 5]

# Lista de ejemplo (agregá hasta 70)
libros = [
    {
        "nombre": "Nocturno de Chile",
        "autor": "Roberto Bolaño",
        "fecha_lanzamiento": "2000-01-01",
        "genero": [4],
        "calificacion": 4,
        "url": "https://example.com/libro-124"
    },
    {
        "nombre": "Los detectives salvajes",
        "autor": "Roberto Bolaño",
        "fecha_lanzamiento": "1998-01-01",
        "genero": [3],
        "calificacion": 4,
        "url": "https://example.com/libro-107"
    },
    {
        "nombre": "2666",
        "autor": "Roberto Bolaño",
        "fecha_lanzamiento": "2004-01-01",
        "genero": [4],
        "calificacion": 5,
        "url": "https://example.com/libro-125"
    },

{
    "nombre": "Matar a un ruiseñor",
    "autor": "Harper Lee",
    "fecha_lanzamiento": "1960-01-01",
    "genero": [4],
    "calificacion": 5,
    "url": "https://example.com/libro-135"
  },
  {
    "nombre": "Tokio Blues",
    "autor": "Haruki Murakami",
    "fecha_lanzamiento": "2002-01-01",
    "genero": [3],
    "calificacion": 4,
    "url": "https://example.com/libro-110"
  },
  {
    "nombre": "Kafka en la orilla",
    "autor": "Haruki Murakami",
    "fecha_lanzamiento": "2002-01-01",
    "genero": [8],
    "calificacion": 4,
    "url": "https://example.com/libro-111"
  },
  {
    "nombre": "La casa de los espíritus",
    "autor": "Isabel Allende",
    "fecha_lanzamiento": "1982-01-01",
    "genero": [1],
    "calificacion": 5,
    "url": "https://example.com/libro-101"
  },
    {
        "nombre": "Pedro Páramo",
        "autor": "Juan Rulfo",
        "fecha_lanzamiento": "1955-01-01",
        "genero": [1],
        "calificacion": 5,
        "url": "https://example.com/libro-127"
    },

    {
        "nombre": "Brida",
        "autor": "Paulo Coelho",
        "fecha_lanzamiento": "1990-01-01",
        "genero": [1],
        "calificacion": 4,
        "url": "https://example.com/libro-200"
    },
    {
        "nombre": "Veronika decide morir",
        "autor": "Paulo Coelho",
        "fecha_lanzamiento": "1998-01-01",
        "genero": [4],
        "calificacion": 5,
        "url": "https://example.com/libro-201"
    },
    {
        "nombre": "El peregrino de Compostela",
        "autor": "Paulo Coelho",
        "fecha_lanzamiento": "1987-01-01",
        "genero": [4],
        "calificacion": 4,
        "url": "https://example.com/libro-202"
    },
    {
        "nombre": "El zorro",
        "autor": "Paulo Coelho",
        "fecha_lanzamiento": "2000-01-01",
        "genero": [7],
        "calificacion": 4,
        "url": "https://example.com/libro-203"
    },
    {
        "nombre": "Once minutos",
        "autor": "Paulo Coelho",
        "fecha_lanzamiento": "2003-01-01",
        "genero": [11],
        "calificacion": 4,
        "url": "https://example.com/libro-204"
    },
    {
        "nombre": "La Quinta Montaña",
        "autor": "Paulo Coelho",
        "fecha_lanzamiento": "1996-01-01",
        "genero": [3],
        "calificacion": 4,
        "url": "https://example.com/libro-205"
    },
    {
        "nombre": "La bruja de Portobello",
        "autor": "Paulo Coelho",
        "fecha_lanzamiento": "2006-01-01",
        "genero": [12],
        "calificacion": 3,
        "url": "https://example.com/libro-206"
    },
    {
        "nombre": "El Demonio y la Señorita Prym",
        "autor": "Paulo Coelho",
        "fecha_lanzamiento": "2000-01-01",
        "genero": [4],
        "calificacion": 4,
        "url": "https://example.com/libro-207"
    },
    {
        "nombre": "El manuscrito encontrado en Accra",
        "autor": "Paulo Coelho",
        "fecha_lanzamiento": "2012-01-01",
        "genero": [4],
        "calificacion": 5,
        "url": "https://example.com/libro-208"
    },
    {
        "nombre": "El vencedor está solo",
        "autor": "Paulo Coelho",
        "fecha_lanzamiento": "2008-01-01",
        "genero": [12],
        "calificacion": 3,
        "url": "https://example.com/libro-209"
    },
    {
        "nombre": "Eva Luna",
        "autor": "Isabel Allende",
        "fecha_lanzamiento": "1987-01-01",
        "genero": [5],
        "calificacion": 5,
        "url": "https://example.com/libro-210"
    },
    {
        "nombre": "Paula",
        "autor": "Isabel Allende",
        "fecha_lanzamiento": "1994-01-01",
        "genero": [4],
        "calificacion": 4,
        "url": "https://example.com/libro-211"
    },
    {
        "nombre": "Retrato en sepia",
        "autor": "Isabel Allende",
        "fecha_lanzamiento": "2000-01-01",
        "genero": [5],
        "calificacion": 4,
        "url": "https://example.com/libro-212"
    },
    {
        "nombre": "La isla bajo el mar",
        "autor": "Isabel Allende",
        "fecha_lanzamiento": "2009-01-01",
        "genero": [3],
        "calificacion": 4,
        "url": "https://example.com/libro-213"
    },
    {
        "nombre": "Inés del alma mía",
        "autor": "Isabel Allende",
        "fecha_lanzamiento": "2006-01-01",
        "genero": [2],
        "calificacion": 5,
        "url": "https://example.com/libro-214"
    },
    {
        "nombre": "El cuaderno de Maya",
        "autor": "Isabel Allende",
        "fecha_lanzamiento": "2011-01-01",
        "genero": [12],
        "calificacion": 3,
        "url": "https://example.com/libro-215"
    },
    {
        "nombre": "La suma de los días",
        "autor": "Isabel Allende",
        "fecha_lanzamiento": "2007-01-01",
        "genero": [4],
        "calificacion": 4,
        "url": "https://example.com/libro-216"
    },
    {
        "nombre": "La madre de Frankenstein",
        "autor": "Isabel Allende",
        "fecha_lanzamiento": "2020-01-01",
        "genero": [12],
        "calificacion": 4,
        "url": "https://example.com/libro-217"
    },
    {
        "nombre": "El país de las mujeres",
        "autor": "Gioconda Belli",
        "fecha_lanzamiento": "1988-01-01",
        "genero": [5],
        "calificacion": 4,
        "url": "https://example.com/libro-218"
    },
    {
        "nombre": "La mujer habitada",
        "autor": "Gioconda Belli",
        "fecha_lanzamiento": "1988-01-01",
        "genero": [4],
        "calificacion": 5,
        "url": "https://example.com/libro-219"
    },
    {
        "nombre": "La casa de Bernarda Alba",
        "autor": "Federico García Lorca",
        "fecha_lanzamiento": "1936-01-01",
        "genero": [4],
        "calificacion": 5,
        "url": "https://example.com/libro-220"
    },
    {
        "nombre": "Bodas de sangre",
        "autor": "Federico García Lorca",
        "fecha_lanzamiento": "1933-01-01",
        "genero": [4],
        "calificacion": 4,
        "url": "https://example.com/libro-221"
    },
    {
        "nombre": "La colmena",
        "autor": "Camilo José Cela",
        "fecha_lanzamiento": "1951-01-01",
        "genero": [2],
        "calificacion": 4,
        "url": "https://example.com/libro-222"
    },
    {
        "nombre": "Don Quijote de la Mancha",
        "autor": "Miguel de Cervantes",
        "fecha_lanzamiento": "1605-01-01",
        "genero": [5],
        "calificacion": 5,
        "url": "https://example.com/libro-223"
    }

]

for libro in libros:
    response = requests.post(API_URL, json=libro, headers=headers)
    if response.status_code == 201:
        print(f"✅ Libro creado: {libro['nombre']}")
    else:
        print(f"❌ Error con: {libro['nombre']}")
        print("Detalles:", response.status_code, response.text)
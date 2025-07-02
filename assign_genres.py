import os
import django
from django.db import transaction # Importa transaction para asegurar la atomicidad
import json # Para cargar datos desde libros.txt

# Configura el entorno de Django
# Reemplaza 'your_project_name' con el nombre real de tu proyecto Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_project.settings')
django.setup()

# Importa tus modelos de la aplicación 'libros'
from libros.models import Libro, Genero

def assign_genres_to_books_from_data():
    """
    Asigna géneros a los libros basándose en los datos proporcionados
    y el archivo libros.txt.
    """
    print("Iniciando el proceso de asignación de géneros a libros desde datos externos...")

    # --- DATOS DE GÉNEROS PROPORCIONADOS POR EL USUARIO ---
    # Usaremos estos para asegurar que los géneros que asignamos existen o se creen correctamente.
    generos_disponibles = [
        { "id": 1, "nombre": "Realismo mágico" },
        { "id": 2, "nombre": "Novela corta" },
        { "id": 3, "nombre": "Ficción" },
        { "id": 4, "nombre": "Drama" },
        { "id": 5, "nombre": "Novela" },
        { "id": 6, "nombre": "Comedia" },
        { "id": 7, "nombre": "Fábula" },
        { "id": 8, "nombre": "Fantasía" },
        { "id": 9, "nombre": "Poesía" },
        { "id": 10, "nombre": "Infantil" },
        { "id": 11, "nombre": "Romance" },
        { "id": 12, "nombre": "Suspenso" },
        { "id": 13, "nombre": "Científico" },
        { "id": 14, "nombre": "Biografía" }
    ]

    # Crear un mapeo de nombre de género a objeto Genero para una búsqueda eficiente
    genre_objects_map = {}
    with transaction.atomic():
        for g_data in generos_disponibles:
            genre_name = g_data['nombre']
            # get_or_create devuelve una tupla (objeto, creado_boolean)
            genre_obj, created = Genero.objects.get_or_create(nombre__iexact=genre_name, defaults={'nombre': genre_name})
            genre_objects_map[genre_name.lower()] = genre_obj
            if created:
                print(f"Género '{genre_name}' creado en la base de datos.")

    # --- Cargar datos de libros desde libros.txt ---
    try:
        # Asume que libros.txt está en la misma carpeta que el script.
        # Si no, ajusta la ruta del archivo.
        with open('libros.txt', 'r', encoding='utf-8') as f:
            libros_data_from_file = json.load(f)
        print(f"Cargados {len(libros_data_from_file)} libros desde 'libros.txt'.")
    except FileNotFoundError:
        print("Error: 'libros.txt' no encontrado. Asegúrate de que el archivo esté en la misma carpeta que el script.")
        return
    except json.JSONDecodeError:
        print("Error: 'libros.txt' no es un archivo JSON válido.")
        return

    # --- Mapeo de libros a géneros (ejemplos) ---
    # Las claves deben coincidir con los nombres de los libros en libros.txt (insensible a mayúsculas/minúsculas).
    # Los valores son listas de nombres de géneros de la lista 'generos_disponibles'.
    book_genre_assignments = {
        "El principito": ["Fábula", "Infantil", "Novela corta"],
        "Cien Años de Soledad": ["Realismo mágico", "Novela", "Ficción"],
        "El amor en los tiempos del cólera": ["Novela", "Romance", "Ficción"],
        "Crónica de una muerte anunciada": ["Novela corta", "Drama", "Ficción"],
        "Harry Potter y la piedra filosofal": ["Fantasía", "Ficción", "Infantil"],
        "Harry Potter y la cámara secreta": ["Fantasía", "Ficción", "Infantil"],
        "Harry Potter y el prisionero de Azkaban": ["Fantasía", "Ficción", "Infantil"],
        "Harry Potter y el Cáliz de Fuego": ["Fantasía", "Ficción"],
        "Harry Potter y la orden del Fénix": ["Fantasía", "Ficción"],
        "Harry Potter y el misterio del Príncipe": ["Fantasía", "Ficción"],
        "Harry Potter y las Reliquias de la Muerte": ["Fantasía", "Ficción"],
        "Animales fantásticos y dónde encontrarlos": ["Fantasía", "Ficción"],
        "Los cuentos de Beedle el Bardo": ["Fantasía", "Fábula", "Infantil"],
        "Yo el Supremo": ["Novela", "Ficción"],
        "Hijo de Hombre": ["Novela", "Ficción"],
        "El trueno entre las Hojas": ["Ficción"],
        "Contravida": ["Novela", "Ficción"],
        "Vigilia del Almirante": ["Novela", "Ficción"],
        "Pirulí": ["Ficción"],
        "El Baldío": ["Ficción"],
        "La Tregua": ["Novela", "Romance", "Drama"],
        "El amor, las mujeres y la vida": ["Poesía", "Romance"],
        "Primavera con una esquina rota": ["Novela", "Drama"],
        "Gracias por el fuego": ["Novela", "Drama"],
        "La borra del café": ["Novela", "Ficción"],
        "La biblioteca de Babel": ["Ficción", "Novela corta"],
        "El Aleph": ["Ficción", "Novela corta"],
        "El sur": ["Ficción", "Novela corta"],
        "Emma Zunz": ["Ficción", "Novela corta"],
        "Poema de los dones": ["Poesía"],
        "Tres versiones de Judas": ["Ficción", "Novela corta"],
        "Pierre Menard, autor del Quijote": ["Ficción", "Novela corta"],
        "El jardín de senderos que se bifurcan": ["Ficción", "Novela corta"],
        "Breve historia del tiempo": ["Científico"],
        "El gran diseño": ["Científico"],
        "El tesoro cósmico": ["Científico", "Infantil"],
        "Breve historia de mi vida": ["Biografía"],
        "Agujeros negros y pequeños universos": ["Científico"],
        "Dios Creó los Números": ["Científico"],
        "La teoría del todo": ["Científico"],
        "Diario de Ana Frank": ["Biografía", "Drama"],
        "El resplandor": ["Suspenso", "Ficción"],
        "Carrie": ["Suspenso", "Ficción"],
        "La Larga Mancha": ["Suspenso", "Ficción"],
        "It (Eso)": ["Suspenso", "Ficción"],
        "1984": ["Distopía", "Novela", "Ficción"],
        "Rebelión en la Granja": ["Fábula", "Ficción"],
        "El Hobbit": ["Fantasía", "Aventura", "Ficción"],
        "El señor de los anillos": ["Fantasía", "Aventura", "Ficción"],
        "Fervor de Buenos Aires": ["Poesía"],
        "El eco del pasado": ["Ficción"],
        "El otoño del patriarca": ["Realismo mágico", "Novela", "Ficción"],
        "El coronel no tiene quien le escriba": ["Novela corta", "Ficción"],
        "Ficciones": ["Ficción", "Novela corta"],
        "Tiempo de cenizas": ["Novela", "Ficción"],
        "El reino de este mundo": ["Realismo mágico", "Novela", "Ficción"],
        "Los pasos perdidos": ["Novela", "Ficción"],
        "Aura": ["Novela corta", "Ficción"],
        "La muerte de Artemio Cruz": ["Novela", "Ficción"],
        "El laberinto de los espíritus": ["Ficción", "Suspenso"],
        "La sombra del viento": ["Ficción", "Suspenso"],
        "Crimen y castigo": ["Novela", "Drama", "Ficción"],
        "Jane Eyre": ["Romance", "Novela", "Drama"],
        "El túnel": ["Novela corta", "Drama", "Ficción"],
        "Fahrenheit 451": ["Ficción", "Científico"], # Asumo "Ciencia Ficción" del anterior, mapeado a "Científico"
        "Nocturno de Chile": ["Novela corta", "Ficción"],
        "Los detectives salvajes": ["Novela", "Ficción"],
        "2666": ["Novela", "Ficción"],
        "Matar a un ruiseñor": ["Drama", "Ficción"],
        "Tokio Blues": ["Novela", "Romance", "Ficción"],
        "Kafka en la orilla": ["Novela", "Fantasía", "Ficción"],
        "La casa de los espíritus": ["Realismo mágico", "Novela", "Ficción"],
        "Pedro Páramo": ["Realismo mágico", "Novela", "Ficción"],
        "Brida": ["Fantasía", "Novela", "Ficción"],
        "Veronika decide morir": ["Novela", "Drama", "Ficción"],
        "El peregrino de Compostela": ["Novela", "Ficción"],
        "El zorro": ["Fábula", "Infantil"],
        "Once minutos": ["Novela", "Romance", "Ficción"],
        "La Quinta Montaña": ["Novela", "Ficción"],
        "La bruja de Portobello": ["Novela", "Fantasía", "Ficción"],
        "El Demonio y la Señorita Prym": ["Novela", "Ficción"],
        "El manuscrito encontrado en Accra": ["Novela", "Ficción"],
        "El vencedor está solo": ["Novela", "Ficción"],
        "Eva Luna": ["Realismo mágico", "Novela", "Ficción"],
        "Paula": ["Biografía", "Drama"],
        "Retrato en sepia": ["Novela", "Ficción"],
        "La isla bajo el mar": ["Novela", "Ficción"],
        "Inés del alma mía": ["Novela", "Ficción"],
        "El cuaderno de Maya": ["Novela", "Ficción"],
        "La suma de los días": ["Biografía", "Ficción"],
        "La madre de Frankenstein": ["Novela", "Ficción"],
        "El país de las mujeres": ["Novela", "Ficción"],
        "La mujer habitada": ["Novela", "Ficción"],
        "La casa de Bernarda Alba": ["Drama"],
        "Bodas de sangre": ["Drama"],
        "La colmena": ["Novela", "Ficción"],
        "Don Quijote de la Mancha": ["Aventura", "Novela", "Ficción"] # "Clásico" no está en tu lista de géneros, lo quito.
    }

    # Usamos una transacción para asegurar que todas las operaciones se completen
    # o se reviertan si ocurre un error.
    with transaction.atomic():
        # Ahora, procesamos cada libro del archivo libros.txt
        for book_data in libros_data_from_file:
            book_name_from_file = book_data['nombre']
            try:
                # Intenta encontrar el libro por su nombre.
                # Usamos __iexact para una búsqueda insensible a mayúsculas/minúsculas.
                book = Libro.objects.get(nombre__iexact=book_name_from_file)
                print(f"\nProcesando libro: '{book.nombre}' (ID: {book.id})")

                # Obtener los nombres de los géneros a asignar para este libro
                # Usamos .get() con un valor por defecto [] si el libro no está en nuestro mapeo
                assigned_genre_names = book_genre_assignments.get(book_name_from_file, [])
                if not assigned_genre_names:
                    print(f"  - No se encontraron géneros definidos para '{book.nombre}' en el mapeo. Saltando asignación de géneros.")
                    continue

                genres_to_add = []
                for genre_name in assigned_genre_names:
                    # Buscamos el objeto Genero usando el mapeo que creamos al inicio
                    genre_obj = genre_objects_map.get(genre_name.lower())
                    if genre_obj:
                        genres_to_add.append(genre_obj)
                    else:
                        print(f"  - Advertencia: El género '{genre_name}' no se encontró en la lista de géneros disponibles o en la base de datos. No se asignará a '{book.nombre}'.")

                if genres_to_add:
                    # Asigna los géneros al libro.
                    # Usamos .set() para reemplazar los géneros existentes con los nuevos.
                    book.generos.set(genres_to_add)
                    print(f"  - Géneros asignados a '{book.nombre}': {[g.nombre for g in genres_to_add]}.")
                else:
                    print(f"  - No se pudieron asignar géneros válidos a '{book.nombre}'.")

            except Libro.DoesNotExist:
                print(f"Advertencia: El libro '{book_name_from_file}' no se encontró en la base de datos. Saltando.")
            except Exception as e:
                print(f"Error al procesar el libro '{book_name_from_file}': {e}")

    print("\nProceso de asignación de géneros completado.")

if __name__ == '__main__':
    assign_genres_to_books_from_data()

import os
import django
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_project.settings')
django.setup()

# Importa tus modelos de la aplicación 'libros'
from libros.models import Libro, Autor, Calificacion, Genero # Importa Genero

def analyze_and_plot_data():
    """
    Función para analizar datos de Django con Pandas y generar gráficos con Matplotlib.
    """
    print("Iniciando análisis de datos y generación de gráficos...")

    # --- 1. Calificaciones promedio de los 20 mejores libros ---
    print("\nGenerando gráfico de calificaciones promedio de los 20 mejores libros...")
    # Obtener todos los libros y sus calificaciones
    # Usamos select_related para optimizar la consulta y evitar N+1
    calificaciones_data = Calificacion.objects.select_related('libro').all()

    # Convertir los datos a un DataFrame de Pandas
    # Creamos una lista de diccionarios para el DataFrame
    data_for_df = []
    for calificacion in calificaciones_data:
        data_for_df.append({
            'libro_nombre': calificacion.libro.nombre,
            'score': calificacion.score
        })

    if not data_for_df:
        print("No hay datos de calificaciones para analizar.")
    else:
        df_calificaciones = pd.DataFrame(data_for_df)

        # Calcular la calificación promedio por libro
        # Group by 'libro_nombre' and calculate the mean of 'score'
        # Luego, ordenar y seleccionar los 20 mejores
        avg_scores = df_calificaciones.groupby('libro_nombre')['score'].mean().sort_values(ascending=False)
        top_20_avg_scores = avg_scores.head(20) # Seleccionar los 20 mejores

        # Crear el gráfico de barras para calificaciones promedio de los 20 mejores
        plt.figure(figsize=(14, 8)) # Tamaño de la figura ajustado para 20 barras
        top_20_avg_scores.plot(kind='bar', color='skyblue') # Tipo de gráfico de barras
        plt.title('Calificación Promedio de los 20 Mejores Libros') # Título del gráfico actualizado
        plt.xlabel('Libro') # Etiqueta del eje X
        plt.ylabel('Calificación Promedio') # Etiqueta del eje Y
        plt.xticks(rotation=45, ha='right') # Rotar etiquetas del eje X para mejor lectura
        plt.yticks(range(0, 6))  # Escala del eje Y de 0 a 5
        plt.grid(axis='y', linestyle='--', alpha=0.7) # Cuadrícula en el eje Y
        plt.tight_layout() # Ajustar el diseño para evitar superposiciones
        plt.show() # Mostrar el gráfico

    # --- 2. Cantidad de libros por autor ---
    print("\nGenerando gráfico de cantidad de libros por autor...")
    # Obtener todos los libros y sus autores
    # Usamos select_related para optimizar la consulta
    libros_data = Libro.objects.select_related('autor').all()

    # Convertir los datos a un DataFrame de Pandas
    data_for_df_autores = []
    for libro in libros_data:
        data_for_df_autores.append({
            'autor_nombre': libro.autor.nombre,
            'libro_nombre': libro.nombre # Incluir el nombre del libro es opcional, pero útil para verificar
        })

    if not data_for_df_autores:
        print("No hay datos de libros para analizar por autor.")
    else:
        df_libros_autores = pd.DataFrame(data_for_df_autores)

        # Contar la cantidad de libros por autor
        # Group by 'autor_nombre' and count the number of books
        libros_por_autor = df_libros_autores['autor_nombre'].value_counts().sort_values(ascending=False)

        # Crear el gráfico de barras para libros por autor
        plt.figure(figsize=(12, 7)) # Tamaño de la figura
        libros_por_autor.plot(kind='bar', color='lightgreen') # Tipo de gráfico de barras
        plt.title('Cantidad de Libros por Autor') # Título del gráfico
        plt.xlabel('Autor') # Etiqueta del eje X
        plt.ylabel('Cantidad de Libros') # Etiqueta del eje Y
        plt.xticks(rotation=45, ha='right') # Rotar etiquetas del eje X
        plt.grid(axis='y', linestyle='--', alpha=0.7) # Cuadrícula en el eje Y
        plt.tight_layout() # Ajustar el diseño
        plt.show() # Mostrar el gráfico

    # --- 3. Cantidad de libros por género ---
    print("\nGenerando gráfico de cantidad de libros por género...")
    # Obtener todos los libros, prefetch_related para obtener los géneros de forma eficiente
    libros_con_generos = Libro.objects.prefetch_related('generos').all()

    # Contar la cantidad de libros por cada género
    genre_counts = {}
    for libro in libros_con_generos:
        for genero in libro.generos.all():
            genre_counts[genero.nombre] = genre_counts.get(genero.nombre, 0) + 1

    if not genre_counts:
        print("No hay datos de géneros o libros asociados a géneros para analizar.")
    else:
        # Convertir el diccionario de conteos a una Serie de Pandas y ordenar
        df_libros_por_genero = pd.Series(genre_counts).sort_values(ascending=False)

        # Crear el gráfico de barras para libros por género
        plt.figure(figsize=(12, 7)) # Tamaño de la figura
        df_libros_por_genero.plot(kind='bar', color='lightcoral') # Tipo de gráfico de barras
        plt.title('Cantidad de Libros por Género') # Título del gráfico
        plt.xlabel('Género') # Etiqueta del eje X
        plt.ylabel('Cantidad de Libros') # Etiqueta del eje Y
        plt.xticks(rotation=45, ha='right') # Rotar etiquetas del eje X
        plt.grid(axis='y', linestyle='--', alpha=0.7) # Cuadrícula en el eje Y
        plt.tight_layout() # Ajustar el diseño
        plt.show() # Mostrar el gráfico


    print("\nAnálisis de datos y generación de gráficos completados.")

if __name__ == '__main__':
    analyze_and_plot_data()

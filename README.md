Sistema de Gestión de Libros (Django REST API)
==============================================

Este proyecto implementa una API RESTful para la gestión de libros, autores, géneros y calificaciones, desarrollada con Django y Django REST Framework. Incluye funcionalidades de autenticación de usuarios y análisis de datos con Pandas y Matplotlib.

📚 Estructura del Proyecto
--------------------------

El proyecto está organizado en las siguientes aplicaciones principales:

* libros: Contiene los modelos, vistas, serializadores y URLs para la gestión de libros, autores, géneros y calificaciones.

* accounts: Maneja el registro y la autenticación de usuarios.

* login\_project (proyecto principal): Contiene la configuración global del proyecto, URLs principales y settings.py.

🚀 Cómo Empezar
---------------

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

### 1\. Versiones de las Herramientas y Librerías

Asegúrate de tener instaladas las siguientes versiones (o superiores) para un funcionamiento óptimo:

* **Python**: 3.9+ (recomendado 3.11)

* **Django**: 4.x

* **Django REST Framework**: 3.x

* **Pandas**: 2.x

* **Matplotlib**: 3.x

* **PostgreSQL**: (Opcional, si usas PostgreSQL como base de datos. SQLite es la base de datos por defecto de Django y no requiere instalación adicional).

### 2\. Instalación y Configuración del Entorno

**1.**  Clonar el repositorio: git clone <https://github.com/Mica569/Libreria-Django.git> 

**2.** Crear un entorno virtual: Un entorno virtual aísla las dependencias de tu proyecto de otras instalaciones de Python.python -m venv venv

3. **Activa el entorno virtual**:
    Windows

    * .\\venv\\Scripts\\activate

    MacOS\\Linux

    * source venv/bin/activate

**4.** Crea un archivo requirements.txt en la raíz de tu proyecto con las siguientes librerías:
```
asgiref==3.8.1
certifi==2025.6.15
charset-normalizer==3.4.2
contourpy==1.3.2
cycler==0.12.1
Django==5.2.1
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
fonttools==4.58.4
idna==3.10
kiwisolver==1.4.8
matplotlib==3.10.3
numpy==2.3.1
packaging==25.0
pandas==2.3.0
pillow==11.2.1
psycopg2-binary==2.9.10
PyJWT==2.9.0
pyparsing==3.2.3
python-dateutil==2.9.0.post0
pytz==2025.2
requests==2.32.4
six==1.17.0
sqlparse==0.5.3
tzdata==2025.2
urllib3==2.5.0
```

Luego, instala:
`pip install -r requirements.txt`

**5.** Por defecto, Django usa SQLite, que no requiere configuración adicional. Si deseas usar PostgreSQL, edita:
login\_project/settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'login',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
(Reemplaza los valores con los de tu base de datos PostgreSQL)_

**6.** Ejecuta en consola
    `python manage.py makemigrations`
    `python manage.py migrate`

**7.** Necesitarás un superusuario para acceder al panel de administración de Django y para probar la autenticación. 
`python manage.py createsuperuser`

**8.** Se puede asignar calificaciones automáticamente a cada libro con el script asign\_calif.py. Este script utiliza un json para cargar las calificaciones (se deben tener ya creados los usuarios y libros para evitar errores con los id), los json se encuentran en la carpeta scripts/json\_data.

`python assign_calif.py`

**9.** Para asignar géneros a tus libros, puedes usar el script assign\_genres.py proporcionado. Asegúrate de que el archivo libros.txt esté en la misma carpeta que el script python assign\_genres.py (Asegúrate de haber personalizado el diccionario book\_genre\_assignments dentro de este script con tus datos.)

`python assign_genres.py`

**10.** Ejecuta
`python manage.py runserver`.

💡 Explicación del Programa y Cómo Funciona
-------------------------------------------

Este proyecto es una API RESTful para un sistema de gestión de libros. Permite a los usuarios interactuar con los datos de libros, autores, géneros y calificaciones a través de endpoints HTTP.

### **Características Principales:**

* **Gestión de Libros**: CRUD (Crear, Leer, Actualizar, Eliminar) para libros.

* **Gestión de Autores**: CRUD para autores.

* **Gestión de Géneros**: CRUD para géneros.

* **Gestión de Calificaciones**: Los usuarios pueden calificar libros.

* **Autenticación de Usuarios**: Registro y login de usuarios con tokens de autenticación.

* **Búsqueda Avanzada de Libros**: Permite buscar libros por nombre, autor y género según calificaciones más altas.

* **Análisis de Datos**: Scripts para generar gráficos a partir de los datos de la base de datos (calificaciones promedio, libros por autor, libros por género).

* **Recomendaciones por Género**: Endpoint para obtener libros mejor calificados dentro de un género específico.

### **Flujo de Trabajo General:**

1. **Registro/Login**: Un usuario se registra o inicia sesión para obtener un token de autenticación.

2. **Acceso a la API**: El usuario incluye este token en los encabezados de sus peticiones a los endpoints protegidos.

3. **Operaciones CRUD**: El usuario puede realizar operaciones sobre los recursos (libros, autores, etc.).

4. **Consultas Especializadas**: El usuario puede usar los endpoints de búsqueda y recomendación.

5. **Análisis Offline**: Los administradores o analistas pueden ejecutar scripts de Python para generar visualizaciones de los datos.

🔑 Autenticación de Usuarios (App accounts)
-------------------------------------------

La aplicación accounts maneja el registro y el inicio de sesión de usuarios.

### Serializador (accounts/serializers.py)

```
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
```

### Vistas (accounts/views.py)

```
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.contrib.auth.models import User

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Credenciales inválidas"}, status=400)
```

### URLs (accounts/urls.py)

```
from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
]
```

### **Peticiones en Postman:**

#### **Registro de Usuario (POST)**

* **URL**: <http://localhost:8000/accounts/register/>

* **Method**: POST

* **Headers**:

  * Content-Type: application/json

```
    {
    "username": "nuevo\_usuario",
    "password": "contrasena"
    }
```
#### **Inicio de Sesión (POST)**

* **URL**: <http://localhost:8000/accounts/login/>

* **Method**: POST

* **Headers**:

  * Content-Type: application/json

```
 { "username": "nuevo_usuario", 
    "password": "contrasena"
}
```
**Respuesta exitosa**:{ "token": "tu\_token\_de\_autenticacion\_aqui"}
**Guarda este token**, lo necesitarás para todas las peticiones a los endpoints protegidos.

#### **Registro de Libro (POST)**

* **URL**: <http://localhost:8000/api/libros/>

* **Method**: POST

* **Headers**:

  * Content-Type: application/json

```
 {
  "nombre": "Nombre del libro",
  "autor": "Nombre del Autor", # Ya debe estar registrado previamente
  "fecha_lanzamiento": "AAAA-MM-DD",
  "url": "www.ejemplo.com"
}
```

**Respuesta exitosa**: Datos del libro registrado

**Las calificaciones y géneros se cargan de forma separada**

#### **Registro de Autor (POST)**

* **URL**: <http://localhost:8000/api/autores/>

* **Method**: POST

* **Headers**:

  * Content-Type: application/json

```
 {
  "nombre": "Nombre del autor",
  "nacionalidad": "Nacionalidad del autor"  
  }
```
**Respuesta exitosa**: Datos del autor registrado

📖 Gestión de Libros (App libros)
---------------------------------

La aplicación libros es el corazón del sistema, permitiendo la gestión de la información relacionada con los libros.

### Modelos (libros/models.py)

```
from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)
    nacionalidad = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    nombre = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    fecha_lanzamiento = models.DateField()
    url = models.CharField(max_length=1000)
    generos = models.ManyToManyField(Genero, related_name='libros_en_genero')

    def __str__(self):
        return f"{self.nombre} - {self.autor.nombre}"

class Calificacion(models.Model):
    class Score(models.IntegerChoices):
        UNO = 1, '1'
        DOS = 2, '2'
        TRES = 3, '3'
        CUATRO = 4, '4'
        CINCO = 5, '5'

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='calificaciones')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calificaciones')
    score = models.IntegerField(choices=Score.choices)
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} → {self.libro.nombre}: {self.score}"
```

### Serializadores (libros/serializers.py)

```
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Autor, Libro, Genero, Calificacion

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class LibroSerializer(serializers.ModelSerializer):
    generos = GeneroSerializer(many=True, read_only=True)

    class Meta:
        model = Libro
        fields = ['id', 'nombre', 'autor', 'fecha_lanzamiento', 'url', 'generos']

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
```

### Vistas (libros/views.py)

```
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q, Avg

from .models import Libro, Autor, Genero, Calificacion
from .serializers import LibroSerializer, AutorSerializer, UserSerializer, GeneroSerializer, CalificacionSerializer
from django.contrib.auth.models import User

# 📘 ABM para LIBROS
class LibroListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            libro = serializer.save()
            return Response(LibroSerializer(libro).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LibroDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Libro.objects.get(pk=pk)
        except Libro.DoesNotExist:
            return None

    def get(self, request, pk):
        libro = self.get_object(pk)
        if libro is None:
            return Response({'error': 'Libro no encontrado'}, status=404)
        serializer = LibroSerializer(libro)
        return Response(serializer.data)

    def put(self, request, pk):
        libro = self.get_object(pk)
        if libro is None:
            return Response({'error': 'Libro no encontrado'}, status=404)
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            libro = serializer.save()
            return Response(LibroSerializer(libro).data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        libro = self.get_object(pk)
        if libro is None:
            return Response({'error': 'Libro no encontrado'}, status=404)
        libro.delete()
        return Response(status=204)

# 🔎 Búsqueda avanzada de libros
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_libros(request):
    nombre = request.GET.get('nombre')
    autor = request.GET.get('autor')
    genero = request.GET.get('genero')
    calificacion_min = request.GET.get('calificacion_min')

    filtros = Q()
    if nombre:
        filtros &= Q(nombre__icontains=nombre)
    if autor:
        filtros &= Q(autor__nombre__icontains=autor)
    if genero:
        filtros &= Q(generos__nombre__icontains=genero)
    if calificacion_min:
        filtros &= Q(calificaciones__score__gte=calificacion_min)

    libros = Libro.objects.filter(filtros).distinct()
    serializer = LibroSerializer(libros, many=True)
    return Response(serializer.data)

# ✍️ ABM para AUTORES
class AutorListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        autores = Autor.objects.all()
        serializer = AutorSerializer(autores, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AutorSerializer(data=request.data)
        if serializer.is_valid():
            autor = serializer.save()
            return Response(AutorSerializer(autor).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AutorDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, nombre):
        try:
            return Autor.objects.get(pk=nombre)
        except Autor.DoesNotExist:
            return None

    def get(self, request, nombre):
        autor = self.get_object(nombre)
        if autor is None:
            return Response({'error': 'Autor no encontrado'}, status=404)
        serializer = AutorSerializer(autor)
        return Response(serializer.data)

    def put(self, request, nombre):
        autor = self.get_object(nombre)
        if autor is None:
            return Response({'error': 'Autor no encontrado'}, status=404)
        serializer = AutorSerializer(autor, data=request.data)
        if serializer.is_valid():
            autor = serializer.save()
            return Response(AutorSerializer(autor).data)
        return Response(serializer.errors, status=400)

    def delete(self, request, nombre):
        autor = self.get_object(nombre)
        if autor is None:
            return Response({'error': 'Autor no encontrado'}, status=404)
        autor.delete()
        return Response(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_autores(request):
    autores = Autor.objects.all()
    serializer = AutorSerializer(autores, many=True)
    return Response(serializer.data)


# 🎨 ABM para GENEROS
class GeneroListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        generos = Genero.objects.all()
        serializer = GeneroSerializer(generos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GeneroSerializer(data=request.data)
        if serializer.is_valid():
            genero = serializer.save()
            return Response(GeneroSerializer(genero).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GeneroDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Genero.objects.get(pk=pk)
        except Genero.DoesNotExist:
            return None

    def get(self, request, pk):
        genero = self.get_object(pk)
        if genero is None:
            return Response({'error': 'Género no encontrado'}, status=404)
        serializer = GeneroSerializer(genero)
        return Response(serializer.data)

    def put(self, request, pk):
        genero = self.get_object(pk)
        if genero is None:
            return Response({'error': 'Género no encontrado'}, status=404)
        serializer = GeneroSerializer(genero, data=request.data)
        if serializer.is_valid():
            genero = serializer.save()
            return Response(GeneroSerializer(genero).data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        genero = self.get_object(pk)
        if genero is None:
            return Response({'error': 'Género no encontrado'}, status=404)
        genero.delete()
        return Response(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_generos(request):
    generos = Genero.objects.all()
    serializer = GeneroSerializer(generos, many=True)
    return Response(serializer.data)

# ⭐ ABM para CALIFICACIONES
class CalificacionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        calificaciones = Calificacion.objects.all()
        serializer = CalificacionSerializer(calificaciones, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CalificacionSerializer(data=request.data)
        if serializer.is_valid():
            calificacion = serializer.save()
            return Response(CalificacionSerializer(calificacion).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CalificacionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Calificacion.objects.get(pk=pk)
        except Calificacion.DoesNotExist:
            return None

    def get(self, request, pk):
        calificacion = self.get_object(pk)
        if calificacion is None:
            return Response({'error': 'Calificación no encontrada'}, status=404)
        serializer = CalificacionSerializer(calificacion)
        return Response(serializer.data)

    def put(self, request, pk):
        calificacion = self.get_object(pk)
        if calificacion is None:
            return Response({'error': 'Calificación no encontrada'}, status=404)
        serializer = CalificacionSerializer(calificacion, data=request.data)
        if serializer.is_valid():
            calificacion = serializer.save()
            return Response(CalificacionSerializer(calificacion).data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        calificacion = self.get_object(pk)
        if calificacion is None:
            return Response({'error': 'Calificación no encontrada'}, status=404)
        calificacion.delete()
        return Response(status=204)

# 👤 Usuarios
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# Nuevo endpoint: Libros mejor calificados por género
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def libros_por_genero_mejor_calificados(request):
    """
    Devuelve una lista de libros con la mejor calificación promedio
    dentro de un género específico, ordenados descendentemente.
    Se puede buscar por 'id' o 'nombre' del género.
    """
    genero_id = request.GET.get('id')
    genero_nombre = request.GET.get('nombre')

    genero = None
    if genero_id:
        try:
            genero = Genero.objects.get(pk=genero_id)
        except Genero.DoesNotExist:
            return Response({'error': 'Género no encontrado por ID'}, status=status.HTTP_404_NOT_FOUND)
    elif genero_nombre:
        try:
            genero = Genero.objects.get(nombre__iexact=genero_nombre)
        except Genero.DoesNotExist:
            return Response({'error': 'Género no encontrado por nombre'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Se requiere un ID o nombre de género para buscar libros.'}, status=status.HTTP_400_BAD_REQUEST)

    if genero:
        libros_mejor_calificados = Libro.objects.filter(
            generos__in=[genero]
        ).annotate(
            average_score=Avg('calificaciones__score')
        ).order_by('-average_score')

        libros_mejor_calificados = libros_mejor_calificados.exclude(average_score__isnull=True)

        if not libros_mejor_calificados.exists():
            return Response({'message': f'No hay libros calificados para el género "{genero.nombre}".'}, status=status.HTTP_200_OK)

        serializer = LibroSerializer(libros_mejor_calificados, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Error interno al procesar la solicitud del género.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

### URLs Principales (login\_project\_/urls.py)

Asegúrate de que tus URLs principales incluyan las URLs de tus aplicaciones libros y accounts.

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('libros/', include('libros.urls')), # Incluye las URLs de tu app 'libros'
    path('accounts/', include('accounts.urls')), # Incluye las URLs de tu app 'accounts'
]
```

📝 Documentación de los Scripts de Carga de Datos
---------------------------------------------

### Script para Asignar Calificaciones a Libros (assign\_calif.py)

Este script de Python se utiliza para asignar estos calificaciones a los libros existentes, basándose en un json user\_1.json, que asigna una calificación usando los id del libro
y del usuario con el que se hizo login previamente.

**Uso:**

1. Haz login con un usuario previamente registrado.

2. Asegúrate de que los jsons estén en la misma carpeta que este script, en otro caso especifica la ruta en el mismo script.

3. Personaliza el json con los ids de tus libros y el del usuario con el que se hizo login, además de las calificaciones que deseas asignar.

   ```
   [
    {
        "score": "2",
        "libro": "1",
        "user": "1"
    }
   ]
   ```

4. Ejecuta el script desde la raíz de tu proyecto Django:
`python assign_calif.py`

**Código del Script:**
```
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

```

### Script para Asignar Géneros a Libros (assign\_genres.py)

Este script de Python se utiliza para poblar la base de datos con géneros y asignar estos géneros a los libros existentes, basándose en un archivo libros.txt y un mapeo predefinido.

**Uso:**

1. Haz una consulta GET para obtener la lista completa de libros y guardalos en un txt. Asegúrate de que libros.txt esté en la misma carpeta que este script.

2. Personaliza el diccionario book\_genre\_assignments dentro del script con los nombres de tus libros y los géneros que deseas asignar.

3. Ejecuta el script desde la raíz de tu proyecto Django:
`python assign_genres.py`

**Código del Script:**
```
import os
import django
from django.db import transaction
import json

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings') # Asegúrate de que 'your_project_name' sea el nombre de tu proyecto principal
django.setup()

from libros.models import Libro, Genero

def assign_genres_to_books_from_data():
    print("Iniciando el proceso de asignación de géneros a libros desde datos externos...")

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

    genre_objects_map = {}
    with transaction.atomic():
        for g_data in generos_disponibles:
            genre_name = g_data['nombre']
            genre_obj, created = Genero.objects.get_or_create(nombre__iexact=genre_name, defaults={'nombre': genre_name})
            genre_objects_map[genre_name.lower()] = genre_obj
            if created:
                print(f"Género '{genre_name}' creado en la base de datos.")

    try:
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
    # PERSONALIZA ESTO CON TUS LIBROS Y GÉNEROS REALES.
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
        "1984": ["Drama", "Novela", "Ficción"],
        "Rebelión en la Granja": ["Fábula", "Ficción"],
        "El Hobbit": ["Fantasía", "Ficción"],
        "El señor de los anillos": ["Fantasía", "Ficción"],
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
        "Fahrenheit 451": ["Ficción", "Científico"],
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
        "Don Quijote de la Mancha": ["Novela", "Ficción"]
    }

    with transaction.atomic():
        for book_data in libros_data_from_file:
            book_name_from_file = book_data['nombre']
            try:
                book = Libro.objects.get(nombre__iexact=book_name_from_file)
                print(f"\nProcesando libro: '{book.nombre}' (ID: {book.id})")

                assigned_genre_names = book_genre_assignments.get(book_name_from_file, [])
                if not assigned_genre_names:
                    print(f"  - No se encontraron géneros definidos para '{book.nombre}' en el mapeo. Saltando asignación de géneros.")
                    continue

                genres_to_add = []
                for genre_name in assigned_genre_names:
                    genre_obj = genre_objects_map.get(genre_name.lower())
                    if genre_obj:
                        genres_to_add.append(genre_obj)
                    else:
                        print(f"  - Advertencia: El género '{genre_name}' no se encontró en la lista de géneros disponibles o en la base de datos. No se asignará a '{book.nombre}'.")

                if genres_to_add:
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
```

📊 Generar y Explicar Gráficos (Uso de Pandas y Matplotlib)
-----------------------------------------------------------

El proyecto incluye un script de Python (analyze\_data.py) que utiliza las librerías pandas y matplotlib para realizar análisis de datos y generar visualizaciones a partir de la información almacenada en la base de datos de Django.

### **Uso del Script de Análisis:**

1. Asegúrate de tener instaladas pandas y matplotlib (pip install pandas matplotlib).

2. Ejecuta el script desde la raíz de tu proyecto Django:

`python analyze_data.py`

Esto generará y mostrará los gráficos en ventanas separadas(En algunos IDEs es necesario cerrar la ventana del gráfico para que se muestre el siguiente).

### **Preguntas y Gráficos Generados:**

El script analyze\_data.py responde visualmente a las siguientes preguntas:

#### **1\. ¿Cuáles son los 20 libros con la mejor calificación promedio?**

Este gráfico de barras muestra la calificación promedio de los 20 libros mejor valorados en el sistema.

[Gráfico: Mejores 20 libros](https://drive.google.com/file/d/13EQayeLunZUTKZr7_YZ4Z-WO3juLOa2s/view?usp=sharing)

#### **2\. ¿Cuántos libros ha escrito cada autor?**

Este gráfico de barras visualiza la cantidad total de libros asociados a cada autor en la base de datos. Siendo Jorge Luis Borges y Paulo Coelho los autores con mayor cantidad de libros registrados, seguidos de Isabel Allende y Joanne Rowling respectivamente.

[Gráfico: Cantidad de libros por autor](https://drive.google.com/file/d/1AXR_BsG2T_QM7tquYlT5v0l4e5q_9Y0g/view?usp=sharing)

#### **3\. ¿Cuántos libros hay por cada género?**

Este gráfico de barras muestra la distribución de libros a través de los diferentes géneros disponibles en el sistema. Se visualiza una gran mayoría en el género Ficción, esto se debe a que la mayoría de los libros registrados tiene más de un género asignado siendo uno de ellos, la mayoría de las veces, ficción.

[Gráfico: Cantidad de libros según género](https://drive.google.com/file/d/1tH2NTlEDHtnlXgt2f2IGvLaVB3URh3nZ/view?usp=sharing)

**Código del Script de Análisis:**
```
import os
import django
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_project.settings') # Asegúrate de que 'login_project' sea el nombre de tu proyecto principal
django.setup()

# Importa tus modelos de la aplicación 'libros'
from libros.models import Libro, Autor, Calificacion, Genero

def analyze_and_plot_data():
    print("Iniciando análisis de datos y generación de gráficos...")

    # --- 1. Calificaciones promedio de los 20 mejores libros ---
    print("\nGenerando gráfico de calificaciones promedio de los 20 mejores libros...")
    calificaciones_data = Calificacion.objects.select_related('libro').all()
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
        avg_scores = df_calificaciones.groupby('libro_nombre')['score'].mean().sort_values(ascending=False)
        top_20_avg_scores = avg_scores.head(20)

        plt.figure(figsize=(14, 8))
        top_20_avg_scores.plot(kind='bar', color='skyblue')
        plt.title('Calificación Promedio de los 20 Mejores Libros')
        plt.xlabel('Libro')
        plt.ylabel('Calificación Promedio')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(range(0, 6))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    # --- 2. Cantidad de libros por autor ---
    print("\nGenerando gráfico de cantidad de libros por autor...")
    libros_data = Libro.objects.select_related('autor').all()
    data_for_df_autores = []
    for libro in libros_data:
        data_for_df_autores.append({
            'autor_nombre': libro.autor.nombre,
            'libro_nombre': libro.nombre
        })

    if not data_for_df_autores:
        print("No hay datos de libros para analizar por autor.")
    else:
        df_libros_autores = pd.DataFrame(data_for_df_autores)
        libros_por_autor = df_libros_autores['autor_nombre'].value_counts().sort_values(ascending=False)

        plt.figure(figsize=(12, 7))
        libros_por_autor.plot(kind='bar', color='lightgreen')
        plt.title('Cantidad de Libros por Autor')
        plt.xlabel('Autor')
        plt.ylabel('Cantidad de Libros')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    # --- 3. Cantidad de libros por género ---
    print("\nGenerando gráfico de cantidad de libros por género...")
    libros_con_generos = Libro.objects.prefetch_related('generos').all()

    genre_counts = {}
    for libro in libros_con_generos:
        for genero in libro.generos.all():
            genre_counts[genero.nombre] = genre_counts.get(genero.nombre, 0) + 1

    if not genre_counts:
        print("No hay datos de géneros o libros asociados a géneros para analizar.")
    else:
        df_libros_por_genero = pd.Series(genre_counts).sort_values(ascending=False)

        plt.figure(figsize=(12, 7))
        df_libros_por_genero.plot(kind='bar', color='lightcoral')
        plt.title('Cantidad de Libros por Género')
        plt.xlabel('Género')
        plt.ylabel('Cantidad de Libros')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    print("\nAnálisis de datos y generación de gráficos completados.")

if __name__ == '__main__':
    analyze_and_plot_data()
```

🎯 Sugerencias por Género Seleccionado (Mejor Valoración)
---------------------------------------------------------

Este endpoint permite obtener una lista de los libros mejor calificados dentro de un género específico.

### **Endpoint:**

* **URL**: <http://localhost:8000/api/generos/libros-mejor-calificados/>

* **Method**: GET

* **Query Params**:

  * id: ID del género (ej. ?id=1)

  * nombre: Nombre del género (ej. ?nombre=Fantasía)

* **Headers**:

  * Authorization: Token

### **Ejemplo de Petición (Postman):**

`GET http://localhost:8000/api/generos/libros-mejor-calificados/?nombre=Drama`
`Authorization: Token tu_token_de_autenticacion`

### Código Relevante (libros/views.py)

```
# libros/views.py (Fragmento de código)
# ... (otras importaciones y clases) ...

from django.db.models import Avg # Asegúrate de importar Avg

# Nuevo endpoint: Libros mejor calificados por género
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def libros_por_genero_mejor_calificados(request):
    """
    Devuelve una lista de libros con la mejor calificación promedio
    dentro de un género específico, ordenados descendentemente.
    Se puede buscar por 'id' o 'nombre' del género.
    """
    genero_id = request.GET.get('id')
    genero_nombre = request.GET.get('nombre')

    genero = None
    if genero_id:
        try:
            genero = Genero.objects.get(pk=genero_id)
        except Genero.DoesNotExist:
            return Response({'error': 'Género no encontrado por ID'}, status=status.HTTP_404_NOT_FOUND)
    elif genero_nombre:
        try:
            genero = Genero.objects.get(nombre__iexact=genero_nombre)
        except Genero.DoesNotExist:
            return Response({'error': 'Género no encontrado por nombre'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Se requiere un ID o nombre de género para buscar libros.'}, status=status.HTTP_400_BAD_REQUEST)

    if genero:
        libros_mejor_calificados = Libro.objects.filter(
            generos__in=[genero]
        ).annotate(
            average_score=Avg('calificaciones__score')
        ).order_by('-average_score')

        libros_mejor_calificados = libros_mejor_calificados.exclude(average_score__isnull=True)

        if not libros_mejor_calificados.exists():
            return Response({'message': f'No hay libros calificados para el género "{genero.nombre}".'}, status=status.HTTP_200_OK)

        serializer = LibroSerializer(libros_mejor_calificados, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Error interno al procesar la solicitud del género.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

⚖️ Licencias
------------

Este proyecto está licenciado bajo los términos de la Licencia MIT.

Puedes usar, copiar, modificar y distribuir este software con o sin fines comerciales, siempre que mantengas el aviso de copyright original y esta licencia.

El proyecto también utiliza varias librerías y herramientas, cada una con su propia licencia. Es importante revisar las licencias de cada componente para asegurar el cumplimiento. Aquí se listan las licencias comunes para las tecnologías utilizadas:

* Python: Python Software Foundation License (PSF)

* Django: BSD 3-Clause License

* Django REST Framework: BSD 3-Clause License

* PostgreSQL: PostgreSQL License

* Pandas: BSD 3-Clause License

* Matplotlib: Matplotlib License (BSD-like)

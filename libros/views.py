from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q, Avg # Importa Avg para calcular promedios

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
    # CORRECCIÓN: Usar 'generos__nombre__icontains' para ManyToManyField
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
            # Búsqueda insensible a mayúsculas/minúsculas para el nombre del género
            genero = Genero.objects.get(nombre__iexact=genero_nombre)
        except Genero.DoesNotExist:
            return Response({'error': 'Género no encontrado por nombre'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Se requiere un ID o nombre de género para buscar libros.'}, status=status.HTTP_400_BAD_REQUEST)

    if genero:
        # Filtrar libros que pertenecen a este género,
        # anotar con el promedio de calificación de sus calificaciones relacionadas,
        # y ordenar por ese promedio de forma descendente.
        libros_mejor_calificados = Libro.objects.filter(
            generos__in=[genero] # Filtra libros que tienen este género asociado
        ).annotate(
            average_score=Avg('calificaciones__score') # Calcula el promedio de las calificaciones de cada libro
        ).order_by('-average_score') # Ordena por el promedio de calificación de forma descendente

        # Excluir libros que no tienen calificaciones (su average_score sería None)
        libros_mejor_calificados = libros_mejor_calificados.exclude(average_score__isnull=True)

        # Si no hay libros con calificaciones para el género
        if not libros_mejor_calificados.exists():
            return Response({'message': f'No hay libros calificados para el género "{genero.nombre}".'}, status=status.HTTP_200_OK)

        # Serializa los libros encontrados.
        # Nota: El 'average_score' no se incluirá en la respuesta a menos que se modifique LibroSerializer
        # para incluirlo, o se cree un serializer personalizado para esta vista.
        serializer = LibroSerializer(libros_mejor_calificados, many=True)
        return Response(serializer.data)
    else:
        # Este caso es un fallback si ninguna de las condiciones de búsqueda de género se cumple.
        return Response({'error': 'Error interno al procesar la solicitud del género.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

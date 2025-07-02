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
    # línea para incluir los géneros en la serialización del libro
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

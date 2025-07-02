from django.db import models
from django.contrib.auth.models import User

#usar pandas para analizar calificaciones
#psycopg buscar
#crear funcion que use un script que use todos los elementos de calif

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
    # ¡NUEVA LÍNEA! Relación Many-to-Many con Genero
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

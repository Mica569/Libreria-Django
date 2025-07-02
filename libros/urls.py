from django.urls import path
from .views import *

urlpatterns = [
    # Libros
    path('libros/', LibroListCreateView.as_view()),
    path('libros/<int:pk>/', LibroDetailView.as_view()),
    path('buscar-libros/', buscar_libros, name='buscar-libros'),
    # NUEVO ENDPOINT: Libros mejor calificados por género
    path('generos/libros-mejor-calificados/', libros_por_genero_mejor_calificados,
         name='libros-por-genero-mejor-calificados'),

    # Autores
    path('autores/', AutorListCreateView.as_view()),
    path('autores/<str:nombre>/', AutorDetailView.as_view()),
    path('autores/', listar_autores, name='listar-autores'),

    # Generos
    path('generos/', GeneroListCreateView.as_view()),
    path('generos/<int:pk>/', GeneroDetailView.as_view()),
    path('generos/', listar_generos, name='listar-generos'),

    # Calificaciones
    path('calificaciones/', CalificacionListCreateView.as_view()),
    path('calificaciones/<int:pk>/', CalificacionDetailView.as_view()),

    # Usuarios
    path('usuarios/', UserListView.as_view()),
]

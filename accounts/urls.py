from django.urls import path
from .views import RegisterView, LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),


]
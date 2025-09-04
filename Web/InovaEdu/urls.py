from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login', views.login, name='login'),
    path('home_Aluno', views.home, name='home'),
    path('cadastro_Aluno', views.cadastro_aluno, name='cadastro_Aluno'),
    path("repositorio", views.repositorio, name="repositorio"),
    path("perfil_A", views.perfil_A, name="perfil_Aluno"),
]

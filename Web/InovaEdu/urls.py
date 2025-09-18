from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('cadastro_Aluno', views.cadastro, name='cadastro_Aluno'),
    path("repositorio", views.repositorio, name="repositorio"),
    path("perfil", views.perfil, name="perfil"),
    path("calendario", views.calendario, name="calendario"),
    path("forum_blocos", views.forum_blocos, name="forum_blocos"),
]
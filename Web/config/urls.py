from django.contrib import admin
from django.urls import path
from InovaEdu import views

urlpatterns = [
    path('', views.login),
    path('login', views.login, name='login'),
    path('home_Aluno', views.home, name='home'),
    path('cadastro_Aluno', views.cadastro_aluno, name='cadastro_Aluno'),

]
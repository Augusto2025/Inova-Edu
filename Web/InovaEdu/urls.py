from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('cadastro_Aluno', views.cadastro, name='cadastro_Aluno'),
    path("repositorio", views.repositorio, name="repositorio"),
    path("perfil", views.perfil, name="perfil"),
    path("calendario", views.calendario, name="calendario"),
    path('lista/', views.lista_usuario, name="lista_usuario"),
    path("forum_blocos", views.forum_blocos, name="forum_blocos"),
    path("curso/<int:curso_id>/turmas", views.turmas, name="turmas"),
    path('home_Coordenacao', views.home_Coordenacao, name="home_Coordenacao"),
    path('cadastroCurso/', views.cadastroCurso, name='cadastroCurso'),
    path('ListaCurso/', views.listacurso, name='lista_curso'),
    path('cadastroTurma/',views.cadastroTurma, name='cadastroTurma'),
    path('listaturma/', views.listaturma, name='listaturma'),
    path('enviar/',views.enviarUsuario,name='enviar'),
    path('usuarios/excluir/<int:idusuario>/', views.excluir_usuario, name='excluir_usuario'),
] 

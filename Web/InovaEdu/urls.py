from django.urls import path
from config import settings 
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.login),
    # Aluno e Professor
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path("repositorio/", views.repositorio, name="repositorio"),
    path("perfil/", views.perfil, name="perfil"),
    path("calendario/", views.calendario, name="calendario"),
    path("forum_blocos/", views.forum_blocos, name="forum_blocos"),
    path('forum/<int:forum_id>/', views.forum_chat, name='forum'),
    path('forum/criar/', views.criar_forum, name='criar_forum'),
    path('calendario/criar/', views.criar_evento, name='criar_evento'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path("curso/<int:curso_id>/turmas/", views.turmas, name="turmas"),
    # Coordenação
    path('home_Coordenacao', views.home_Coordenacao, name="home_Coordenacao"),
    path('cadastro_Aluno/', views.cadastro, name='cadastro_Aluno'),
    path('cadastroCurso/', views.cadastroCurso, name='cadastroCurso'),
    path('cadastroTurma/',views.cadastroTurma, name='cadastroTurma'),
    path('listaturma/', views.listaturma, name='listaturma'),
    path('usuarios/excluir/<int:idusuario>/', views.excluir_usuario, name='excluir_usuario'),
    path('enviarturma/', views.enviarturma, name='enviarturma'),
    path('criar_curso', views.criar_curso, name='criar_curso'),
    path('curso/lista/', views.lista_curso, name='ListaCurso'),
    path('lista/', views.lista_usuario, name="lista_usuario"),
] 

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
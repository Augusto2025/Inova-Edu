from django.urls import path
from config import settings  # Corrigido para importar de 'config'
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homePage),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('cadastro_Aluno', views.cadastro, name='cadastro_Aluno'),
    path("repositorio", views.repositorio, name="repositorio"),
    path("perfil", views.perfil, name="perfil"),
    path("calendario", views.calendario, name="calendario"),
    path('lista/', views.lista_usuario, name="lista_usuario"),
    path("forum_blocos", views.forum_blocos, name="forum_blocos"),
    path('forum/criar/', views.criar_forum, name='criar_forum'),
    path('evento/criar/', views.criar_evento, name='criar_evento'),
    path("curso/<int:curso_id>/turmas", views.turmas, name="turmas"),
    path('home_Coordenacao', views.home_Coordenacao, name="home_Coordenacao"),
    path('cadastroCurso/', views.cadastroCurso, name='cadastroCurso'),
    path('cadastroTurma/',views.cadastroTurma, name='cadastroTurma'),
    path('listaturma/', views.listaturma, name='listaturma'),
    path('enviar/',views.enviarUsuario,name='enviar'),
    path('usuarios/excluir/<int:idusuario>/', views.excluir_usuario, name='excluir_usuario'),
    path('forum/<int:forum_id>/', views.forum_chat, name='forum'),
    path('enviarturma/', views.enviarturma, name='enviarturma'),
    path('criar_curso', views.criar_curso, name='criar_curso'),
    path('curso/lista/', views.lista_curso, name='ListaCurso'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('upload/', views.upload_arquivo, name='upload_arquivo'),
    path('pasta/<int:pasta_id>/', views.abrir_pasta, name='abrir_pasta'),
    path('pasta/<int:pasta_id>/criar_pasta/', views.criar_pasta, name='criar_pasta'),  # Certifique-se de que essa linha existe
    path('pasta/<int:pasta_id>/criar_arquivo/', views.criar_arquivo, name='criar_arquivo'),
    path('reSenha', views.reSenha, name='reSenha'),
]

# Serve arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

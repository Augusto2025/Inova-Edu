from django.urls import path
from config import settings 
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.homePage),
    path('login/', views.login, name='login'),
    path('redefinir_senha', views.redefinir_senha, name='redefinir_senha'),
    path("pedir_email/", views.pedir_email, name="pedir_email"),
    path("verificar-codigo/", views.verificar_codigo, name="verificar_codigo"),
    # Aluno e Professor
    path('home/', views.home, name='home'),
    path("perfil/", views.perfil, name="perfil"),
    path("calendario/", views.calendario, name="calendario"),
    path("forum_blocos/", views.forum_blocos, name="forum_blocos"),
    path('forum/<int:forum_id>/', views.forum_chat, name='forum'),
    path('forum/criar/', views.criar_forum, name='criar_forum'),
    path('calendario/criar/', views.criar_evento, name='criar_evento'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path("curso/<int:curso_id>/turmas/", views.turmas, name="turmas"),
    path('repositorio/<int:turma_id>/', views.repositorio, name='repositorio'),
    path('repositorio/pasta/<int:pasta_id>/', views.repositorio_pasta, name='repositorio_pasta'),
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
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
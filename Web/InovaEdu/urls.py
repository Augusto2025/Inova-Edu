from django.urls import path
from config import settings 
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.homePage),
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
    path('home_Coordenacao/', views.home_Coordenacao, name="home_Coordenacao"),
    path('criar_curso/', views.criar_curso, name='criar_curso'),
    path('criar_turma/', views.criar_turma, name='criar_turma'),
    
    path('usuarios/editar/<int:idusuario>/', views.editar_usuario, name='editar_usuario'),
    path("curso/editar/", views.editar_curso, name="editar_curso"),
    path('turma/editar/', views.editar_turma, name='editar_turma'),

    path('usuarios/excluir/<int:idusuario>/', views.excluir_usuario, name='excluir_usuario'),
    path('curso/excluir/<int:idcurso>/', views.excluir_curso, name='excluir_curso'),
    path('turma/excluir/<int:idturma>/', views.excluir_turma, name='excluir_turma'),



    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('redefinir_senha', views.redefinir_senha, name='redefinir_senha'),
    path("pedir_email/", views.pedir_email, name="pedir_email"),
    path("verificar-codigo/", views.verificar_codigo, name="verificar_codigo"),
    
    
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
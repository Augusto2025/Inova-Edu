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
    
    # NOVAS URLs para o perfil AJAX
    path('api/atualizar-perfil/', views.atualizar_perfil_ajax, name='atualizar_perfil_ajax'),
    path('api/upload-foto/', views.upload_foto_ajax, name='upload_foto_ajax'),
    path('api/cursos/', views.gerenciar_cursos_ajax, name='gerenciar_cursos_ajax'),
    path('api/projetos/', views.listar_projetos_ajax, name='listar_projetos_ajax'),
    
    path("calendario/", views.calendario, name="calendario"),
    path("forum_blocos/", views.forum_blocos, name="forum_blocos"),
    path("forum/<int:idforum>/topicos/",views.forum_topicos,name="forum_topicos"),
    path('forum/<int:forum_id>/', views.forum_chat, name='forum'),
    path('forum/criar/', views.criar_forum, name='criar_forum'),
    path('forum/excluir/<int:forum_id>/', views.excluir_forum, name='excluir_forum'),
    path('forum/editar/<int:forum_id>/', views.editar_forum, name='editar_forum'),
    path('calendario/criar/', views.criar_evento, name='criar_evento'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path("curso/<int:curso_id>/turmas/", views.turmas, name="turmas"),
    path('repositorio/<int:turma_id>/', views.repositorio, name='repositorio'),
    path('repositorio/pasta/<int:pasta_id>/', views.repositorio_pasta, name='repositorio_pasta'),
    
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
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
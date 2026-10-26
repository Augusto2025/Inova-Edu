"""
Views package for InovaEdu.
Organized by functional area for maintainability.
"""

# Authentication
from .auth_views import (
    login,
    csrf_failure,
)

# Aluno/Professor area
from .aluno_professor_views import (
    HomeAlunoProfessor,
    perfil,
    atualizar_perfil_ajax,
    upload_foto,
    cursos,
    turmas,
    calendario,
    criar_evento,
    editar_evento,
    excluir_evento,
    forum_blocos,
    criar_forum,
    editar_forum,
    excluir_forum,
    forum_topicos,
    criar_topico,
    editar_topico,
    excluir_topico,
    forum_chat,
    excluir_mensagem,
    editar_mensagem,
    buscar_novas_mensagens,
)

# Coordenação area
from .coordenacao_views import (
    HomeCoord,
    UsuarioCoord,
    listar_alunos,
    salvar_alunos_turma,
    editar_usuario,
    excluir_usuario,
    CursoCoord,
    criar_curso,
    editar_curso,
    excluir_curso,
    TurmaCoord,
    criar_turma,
    editar_turma,
    excluir_turma,
    listar_alunos_turma,
    salvar_turma_usuario,
    projetosCoord,
)

# Projects & Repository
from .projeto_views import (
    projetos_da_turma,
    repositorio_projeto,
    repositorio_pasta,
    download_repositorio_projeto,
)

# Certificates
from .certificado_views import (
    salvar_certificado,
)

# API endpoints
from .api_views import (
    listar_projetos_ajax,
)

# Home page
from .home_views import (
    homePage,
)

# Utility functions (for internal use)
from .utils import (
    safe_redirect,
    validate_file_upload,
    sanitize_filename,
    upload_para_cloudinary,
    adicionar_pasta_ao_zip,
    usuario_pode_editar_projeto,
    ALLOWED_FILE_EXTENSIONS,
    MAX_FILE_SIZE,
    BLOCKED_MIME_TYPES,
)

__all__ = [
    # Auth
    'login',
    'csrf_failure',
    # Aluno/Professor
    'HomeAlunoProfessor',
    'perfil',
    'atualizar_perfil_ajax',
    'upload_foto',
    'cursos',
    'turmas',
    'calendario',
    'criar_evento',
    'editar_evento',
    'excluir_evento',
    'forum_blocos',
    'criar_forum',
    'editar_forum',
    'excluir_forum',
    'forum_topicos',
    'criar_topico',
    'editar_topico',
    'excluir_topico',
    'forum_chat',
    'excluir_mensagem',
    'editar_mensagem',
    'buscar_novas_mensagens',
    # Coordenação
    'HomeCoord',
    'UsuarioCoord',
    'listar_alunos',
    'salvar_alunos_turma',
    'editar_usuario',
    'excluir_usuario',
    'CursoCoord',
    'criar_curso',
    'editar_curso',
    'excluir_curso',
    'TurmaCoord',
    'criar_turma',
    'editar_turma',
    'excluir_turma',
    'listar_alunos_turma',
    'salvar_turma_usuario',
    'projetosCoord',
    # Projects
    'projetos_da_turma',
    'repositorio_projeto',
    'repositorio_pasta',
    'download_repositorio_projeto',
    # Certificates
    'salvar_certificado',
    # API
    'listar_projetos_ajax',
    # Home
    'homePage',
    # Utils
    'safe_redirect',
    'validate_file_upload',
    'sanitize_filename',
    'upload_para_cloudinary',
    'adicionar_pasta_ao_zip',
    'usuario_pode_editar_projeto',
    'ALLOWED_FILE_EXTENSIONS',
    'MAX_FILE_SIZE',
    'BLOCKED_MIME_TYPES',
]
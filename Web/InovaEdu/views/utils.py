"""
Utility functions shared across views.
"""
import re
import os
import io
import json
import zipfile
import requests
import logging
from datetime import timedelta
from urllib.parse import urlparse

from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.utils import timezone
from django.conf import settings

from cloudinary import uploader
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload as cloudinary_upload

from ..models import (
    Usuario, Turma, Projeto, Pasta, Arquivo,
    UsuarioDaTurma, Forum, Topico, Mensagem, Eventos, Certificado
)

logger = logging.getLogger(__name__)


# =========================================================================
# File Upload Validation
# =========================================================================

# Extensões de arquivo permitidas para upload
ALLOWED_FILE_EXTENSIONS = {
    # Documentos
    '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt',
    # Planilhas
    '.xls', '.xlsx', '.csv', '.ods',
    # Apresentações
    '.ppt', '.pptx', '.odp',
    # Imagens
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg',
    # Código/Desenvolvimento
    '.py', '.js', '.ts', '.html', '.css', '.json', '.xml', '.yaml', '.yml',
    '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs',
    # Arquivos compactados
    '.zip', '.rar', '.7z', '.tar', '.gz',
    # Outros
    '.md', '.log', '.sql'
}

# Tamanho máximo de arquivo (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# MIME types perigosos que devem ser bloqueados
BLOCKED_MIME_TYPES = {
    'application/x-msdownload',      # .exe
    'application/x-msdos-program',   # .com
    'application/x-sh',              # .sh
    'application/x-python-code',     # .pyc
    'application/x-php',             # .php
    'text/x-php',                    # .php
    'application/javascript',        # .js (pode ser perigoso se executado no servidor)
}


def sanitize_filename(filename):
    """Sanitize filename to prevent path traversal and injection."""
    return re.sub(r"[^A-Za-z0-9._-]", "_", filename)


def validate_file_upload(arquivo_file):
    """
    Valida o arquivo enviado: extensão, tamanho e MIME type.
    Retorna (is_valid, error_message).
    """
    if not arquivo_file:
        return False, "Nenhum arquivo foi enviado."

    # Verificar tamanho
    if arquivo_file.size > MAX_FILE_SIZE:
        return False, f"Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE // (1024*1024)}MB."

    # Verificar extensão
    _, ext = os.path.splitext(arquivo_file.name.lower())
    if ext not in ALLOWED_FILE_EXTENSIONS:
        return False, f"Extensão de arquivo não permitida: {ext}. Extensões permitidas: {', '.join(sorted(ALLOWED_FILE_EXTENSIONS))}"

    # Verificar MIME type (content_type do arquivo)
    content_type = getattr(arquivo_file, 'content_type', None)
    if content_type and content_type in BLOCKED_MIME_TYPES:
        return False, f"Tipo de arquivo não permitido: {content_type}"

    return True, None


def upload_para_cloudinary(arquivo_file, public_id):
    """Upload file to Cloudinary and return (public_id, resource_type, url)."""
    resultado = cloudinary_upload(
        arquivo_file, resource_type="raw", public_id=public_id, overwrite=True
    )
    resource_type = resultado.get("resource_type", "raw")
    public_id_str = str(resultado["public_id"])
    url = cloudinary_url(
        public_id_str, resource_type=resource_type, version=resultado.get("version")
    )[0]
    return public_id_str, resource_type, url


def adicionar_pasta_ao_zip(zip_file, projeto, pasta=None, caminho=""):
    """Recursively add folder contents to zip file."""
    arquivos = Arquivo.objects.filter(projeto=projeto, pasta=pasta)
    for arquivo in arquivos:
        if arquivo.url:
            try:
                r = requests.get(arquivo.url, timeout=10)
                if r.status_code == 200:
                    zip_file.writestr(f"{caminho}{arquivo.nome}", r.content)
            except requests.RequestException:
                pass  # Previne travamento caso algum arquivo específico falhe

    subpastas = Pasta.objects.filter(projeto=projeto, pasta_pai=pasta)
    for subpasta in subpastas:
        adicionar_pasta_ao_zip(
            zip_file, projeto, subpasta, f"{caminho}{subpasta.nome}/"
        )


# =========================================================================
# Security & Redirect Helpers
# =========================================================================

def safe_redirect(request, fallback_url_name):
    """
    Safely redirect to HTTP_REFERER if it's on the same domain, otherwise fallback.
    Prevents open redirect vulnerabilities (CWE-601).
    """
    referer = request.META.get('HTTP_REFERER')
    if referer:
        try:
            parsed_referer = urlparse(referer)
            parsed_current = urlparse(request.build_absolute_uri('/'))
            # Only allow redirect if same domain
            if parsed_referer.netloc == parsed_current.netloc:
                return redirect(referer)
        except Exception:
            pass
    return redirect(fallback_url_name)


def usuario_pode_editar_projeto(usuario, projeto):
    """
    Auxiliar para verificar se um determinado usuário pode editar um projeto específico.
    """
    if not usuario or not projeto:
        return False

    # É o professor da turma?
    if projeto.turma and projeto.turma.professor:
        if usuario.idusuario == projeto.turma.professor.idusuario:
            return True

    # O aluno está na lista de permissões de edição?
    if projeto.alunos_edicao.filter(idusuario=usuario.idusuario).exists():
        return True

    return False


def get_usuario_from_session(request):
    """Extract authenticated usuario from session, or return None."""
    email = request.session.get('usuario_email')
    if not email:
        return None
    try:
        return Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return None


def require_login(view_func):
    """Decorator to require authenticated user."""
    def wrapper(request, *args, **kwargs):
        usuario = get_usuario_from_session(request)
        if not usuario:
            return redirect('login')
        request.usuario = usuario
        return view_func(request, *args, **kwargs)
    return wrapper


def require_coordenador(view_func):
    """Decorator to require coordenador role."""
    def wrapper(request, *args, **kwargs):
        usuario = get_usuario_from_session(request)
        if not usuario or usuario.tipo != 'Coordenador':
            return redirect('home')
        request.usuario = usuario
        return view_func(request, *args, **kwargs)
    return wrapper


def require_professor_da_turma(view_func):
    """Decorator to require user is professor of the turma (via turma_id kwarg)."""
    def wrapper(request, *args, **kwargs):
        usuario = get_usuario_from_session(request)
        if not usuario:
            return redirect('login')

        turma_id = kwargs.get('turma_id') or kwargs.get('idturma')
        if turma_id:
            turma = get_object_or_404(Turma, idturma=turma_id)
            if not (turma.professor and usuario.idusuario == turma.professor.idusuario):
                return redirect('home')

        request.usuario = usuario
        return view_func(request, *args, **kwargs)
    return wrapper
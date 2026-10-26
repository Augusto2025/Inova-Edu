"""
API endpoints for AJAX requests.
Require authentication.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q

from ..models import Projeto, Usuario
from .utils import get_usuario_from_session, require_login


@require_GET
@require_login
def listar_projetos_ajax(request):
    """
    Retorna a lista de projetos associados ao usuário logado via JSON.
    """
    usuario = request.usuario

    # Busca projetos onde o usuário é aluno participante OU possui permissão de edição
    projetos = (
        Projeto.objects.filter(Q(alunos=usuario) | Q(alunos_edicao=usuario))
        .distinct()
        .select_related("turma")
    )

    lista_projetos = []
    for projeto in projetos:
        data_formatada = (
            projeto.data_de_criacao.strftime("%d/%m/%Y")
            if getattr(projeto, "data_de_criacao", None)
            else None
        )

        lista_projetos.append(
            {
                "id": projeto.idprojeto,
                "titulo": projeto.nome_projeto,
                "descricao": projeto.descricao or "",
                "turma": projeto.turma.codigo_turma if (projeto.turma and hasattr(projeto.turma, 'codigo_turma')) else None,
                "data_criacao": data_formatada,
                "imagem_url": projeto.imagem.url if projeto.imagem else None,
            }
        )

    return JsonResponse({"projetos": lista_projetos})
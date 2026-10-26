"""
Coordenação (Admin) area views.
All views require Coordenador role.
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages

from ..models import (
    Usuario, Curso, Turma, Projeto, UsuarioDaTurma
)
from .utils import get_usuario_from_session, require_coordenador


# =========================================================================
# COORDENAÇÃO - HOME
# =========================================================================

@require_coordenador
def HomeCoord(request):
    """Dashboard da coordenação."""
    usuario = request.usuario

    total_usuarios = Usuario.objects.count()
    total_cursos = Curso.objects.count()
    total_turmas = Turma.objects.count()

    projetos = Projeto.objects.select_related(
        "turma",
        "turma__curso"
    ).prefetch_related(
        "alunos",
        "alunos_edicao"
    ).all().order_by("-data_de_criacao")

    context = {
        "total_usuarios": total_usuarios,
        "total_cursos": total_cursos,
        "total_turmas": total_turmas,
        "projetos": projetos,
        "usuario": usuario,
    }

    return render(request, "Coordenacao/HomeCoord.html", context)


# =========================================================================
# USUÁRIOS
# =========================================================================

@require_coordenador
def UsuarioCoord(request):
    """Gerenciamento de usuários."""
    usuario = request.usuario

    if request.method == "POST":
        acao = request.POST.get("acao")

        if acao == "cadastrar_usuario":
            email = request.POST.get("email")

            if Usuario.objects.filter(email=email).exists():
                messages.error(request, "Este e-mail já está cadastrado!")
                return redirect("UsuariosCoord")

            novo_usuario = Usuario(
                nome=request.POST.get("nome"),
                sobrenome=request.POST.get("sobrenome"),
                email=email,
                descricao=request.POST.get("descricao"),
                tipo=request.POST.get("tipoCadastro"),
                imagem=request.FILES.get("imagem"),
            )
            novo_usuario.set_password(request.POST.get("senha"))
            novo_usuario.save()

            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect("UsuariosCoord")

    filtro = request.GET.get("tipo", "todos")

    usuarios = Usuario.objects.all()

    if filtro == "professor":
        usuarios = usuarios.filter(tipo__iexact="Professor")
    elif filtro == "aluno":
        usuarios = usuarios.filter(tipo__iexact="Aluno")
    elif filtro == "coordenador":
        usuarios = usuarios.filter(tipo__iexact="Coordenador")

    context = {
        "usuarios": usuarios,
        "total_usuarios": Usuario.objects.count(),
        "total_professores": Usuario.objects.filter(tipo__iexact="Professor").count(),
        "total_alunos": Usuario.objects.filter(tipo__iexact="Aluno").count(),
        "total_coordenadores": Usuario.objects.filter(tipo__iexact="Coordenador").count(),
        "filtro": filtro,
        "usuario": usuario,
    }

    return render(request, "Coordenacao/UsuarioCoord.html", context)


@require_coordenador
def listar_alunos(request):
    """API: listar alunos e professores para seleção."""
    alunos = Usuario.objects.filter(tipo__in=['Aluno', 'Professor'])

    data = [
        {
            "id": aluno.idusuario,
            "nome": aluno.nome,
            "sobrenome": aluno.sobrenome
        }
        for aluno in alunos
    ]

    return JsonResponse(data, safe=False)


@require_POST
@require_coordenador
def salvar_alunos_turma(request):
    """Salvar associação alunos-turma."""
    try:
        data = json.loads(request.body)

        turma_id = data.get("turma")
        alunos_ids = data.get("alunos", [])

        turma = Turma.objects.get(idturma=turma_id)

        # Remove todos vínculos antigos
        UsuarioDaTurma.objects.filter(id_turma=turma).delete()

        for aluno_id in alunos_ids:
            try:
                aluno = Usuario.objects.get(idusuario=aluno_id)
                if aluno.tipo.lower() in ["aluno", "professor"]:
                    UsuarioDaTurma.objects.create(
                        id_usuario=aluno,
                        id_turma=turma
                    )
            except Usuario.DoesNotExist:
                continue

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"status": "erro", "msg": str(e)})


@require_coordenador
def editar_usuario(request, idusuario):
    """Editar usuário."""
    usuario_logado = request.usuario
    usuario = get_object_or_404(Usuario, idusuario=idusuario)

    if request.method == "POST":
        usuario.nome = request.POST.get("nome")
        usuario.sobrenome = request.POST.get("sobrenome")
        usuario.email = request.POST.get("email")
        usuario.descricao = request.POST.get("descricao")
        usuario.tipo = request.POST.get("tipoCadastro")

        if request.FILES.get("imagem"):
            usuario.imagem = request.FILES.get("imagem")

        usuario.save()

        messages.success(request, "Usuário atualizado com sucesso!")
        return redirect("UsuariosCoord")

    return render(request, "Coordenacao/EditarUsuario.html", {"usuario": usuario, "usuario_logado": usuario_logado})


@require_coordenador
def excluir_usuario(request, idusuario):
    """Excluir usuário."""
    if request.method == "POST":
        usuario = get_object_or_404(Usuario, idusuario=idusuario)
        usuario.delete()
        messages.success(request, "Usuário excluído com sucesso!")

    return redirect("UsuariosCoord")


# =========================================================================
# CURSOS
# =========================================================================

@require_coordenador
def CursoCoord(request):
    """Gerenciamento de cursos."""
    usuario = request.usuario
    cursos = Curso.objects.all().order_by("nome_curso")

    return render(request, "Coordenacao/CursoCoord.html", {
        "cursos": cursos,
        "usuario": usuario
    })


@require_coordenador
def criar_curso(request):
    """Criar novo curso."""
    usuario = request.usuario

    if request.method == "POST":
        Curso.objects.create(
            nome_curso=request.POST.get("nome_curso"),
            descricao_curso=request.POST.get("descricao_curso"),
            data_inicio=request.POST.get("data_inicio") or None,
            data_final=request.POST.get("data_final") or None,
            imagem=request.FILES.get("imagem"),
            usuario=usuario,
        )
        messages.success(request, "Curso cadastrado com sucesso!")
        return redirect("CursoCoord")

    return redirect("CursoCoord")


@require_coordenador
def editar_curso(request):
    """Editar curso."""
    if request.method == "POST":
        curso = get_object_or_404(Curso, idcurso=request.POST.get("idcurso"))

        curso.nome_curso = request.POST.get("nome_curso")
        curso.data_inicio = request.POST.get("data_inicio")
        curso.data_final = request.POST.get("data_final")
        curso.descricao_curso = request.POST.get("descricao_curso")

        if request.FILES.get("imagem"):
            curso.imagem = request.FILES.get("imagem")

        curso.save()
        messages.success(request, "Curso atualizado com sucesso!")

    return redirect("CursoCoord")


@require_coordenador
def excluir_curso(request, idcurso):
    """Excluir curso."""
    if request.method == "POST":
        curso = get_object_or_404(Curso, idcurso=idcurso)
        curso.delete()
        messages.success(request, "Curso excluído com sucesso!")

    return redirect("CursoCoord")


# =========================================================================
# TURMAS
# =========================================================================

@require_coordenador
def TurmaCoord(request):
    """Gerenciamento de turmas."""
    usuario = request.usuario

    turmas = Turma.objects.select_related("curso", "professor").all()
    cursos = Curso.objects.all()
    professores = Usuario.objects.filter(tipo="Professor")
    alunos = Usuario.objects.filter(tipo="Aluno")

    context = {
        "turmas": turmas,
        "cursos": cursos,
        "professores": professores,
        "alunos": alunos,
        "usuario": usuario,
    }

    return render(request, "Coordenacao/TurmaCoord.html", context)


@require_coordenador
def criar_turma(request):
    """Criar nova turma."""
    if request.method == "POST":
        codigo_turma = request.POST.get("codigo_turma")
        turno = request.POST.get("turno")
        ano = request.POST.get("ano")
        curso_id = request.POST.get("curso_id")
        professor_id = request.POST.get("professor_id")

        curso = get_object_or_404(Curso, idcurso=curso_id)
        professor = get_object_or_404(Usuario, idusuario=professor_id)

        Turma.objects.create(
            codigo_turma=codigo_turma,
            turno=turno,
            ano=ano,
            curso=curso,
            professor=professor,
        )

        messages.success(request, "Turma cadastrada com sucesso!")
        return redirect("TurmaCoord")

    return redirect("TurmaCoord")


@require_coordenador
def editar_turma(request):
    """Editar turma."""
    if request.method == "POST":
        turma = get_object_or_404(Turma, idturma=request.POST.get("idturma"))

        turma.codigo_turma = request.POST.get("codigo_turma")
        turma.turno = request.POST.get("turno")
        turma.ano = request.POST.get("ano")
        turma.curso_id = request.POST.get("curso")
        turma.professor_id = request.POST.get("professor_id")

        turma.save()
        messages.success(request, "Turma atualizada com sucesso!")

    return redirect("TurmaCoord")


@require_coordenador
def excluir_turma(request, idturma):
    """Excluir turma."""
    turma = get_object_or_404(Turma, idturma=idturma)

    if request.method == "POST":
        turma.delete()
        messages.success(request, "Turma excluída com sucesso!")

    return redirect("TurmaCoord")


@require_coordenador
def listar_alunos_turma(request, idturma):
    """API: listar alunos de uma turma."""
    alunos = UsuarioDaTurma.objects.filter(
        id_turma_id=idturma
    ).values_list("id_usuario_id", flat=True)

    return JsonResponse({"alunos": list(alunos)})


@require_POST
@require_coordenador
def salvar_turma_usuario(request):
    """Salvar associação turma-usuário (coordenador)."""
    dados = json.loads(request.body)

    turma = Turma.objects.get(idturma=dados["turma"])
    ids = dados["usuarios"]

    UsuarioDaTurma.objects.filter(id_turma=turma).delete()

    for id_usuario in ids:
        UsuarioDaTurma.objects.create(
            id_turma=turma,
            id_usuario=Usuario.objects.get(idusuario=id_usuario)
        )

    return JsonResponse({"status": "ok"})


# =========================================================================
# PROJETOS (Coordenação)
# =========================================================================

@require_coordenador
def projetosCoord(request):
    """Dashboard de projetos para coordenação."""
    usuario = request.usuario

    total_usuarios = Usuario.objects.count()
    total_cursos = Curso.objects.count()
    total_turmas = Turma.objects.count()

    projetos = Projeto.objects.select_related(
        "turma",
        "turma__curso"
    ).prefetch_related(
        "alunos",
        "alunos_edicao"
    ).all().order_by("nome_projeto")

    context = {
        "total_usuarios": total_usuarios,
        "total_cursos": total_cursos,
        "total_turmas": total_turmas,
        "projetos": projetos,
        "usuario": usuario,
    }

    return render(request, "Coordenacao/projetosCoord.html", context)
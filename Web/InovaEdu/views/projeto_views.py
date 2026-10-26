"""
Project and Repository views.
Require authentication + authorization checks.
"""
import io
import zipfile
import json
import requests
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from django.contrib import messages
from django.db.models import Q

from ..models import (
    Usuario, Turma, Projeto, Pasta, Arquivo, UsuarioDaTurma, Certificado
)
from .utils import (
    get_usuario_from_session, require_login,
    validate_file_upload, sanitize_filename, upload_para_cloudinary,
    adicionar_pasta_ao_zip, usuario_pode_editar_projeto
)


# =========================================================================
# PROJETOS DA TURMA
# =========================================================================

@require_login
def projetos_da_turma(request, turma_id):
    """
    View principal para listagem, cadastro, edição, exclusão e permissões dos projetos da turma.
    """
    turma = get_object_or_404(Turma, idturma=turma_id)
    projetos = Projeto.objects.filter(turma=turma)

    usuario = request.usuario

    # Verifica se o usuário é o Professor da Turma
    is_professor = False
    if turma.professor:
        is_professor = (usuario.idusuario == turma.professor.idusuario)

    can_modify = is_professor

    if request.method == "POST":
        header_xhr = request.headers.get("x-requested-with", "") or request.headers.get("X-Requested-With", "")
        is_ajax = header_xhr.lower() == "xmlhttprequest"

        action = request.POST.get("action")

        # 1. CADASTRAR PROJETO
        if action == "cadastrar_projeto":
            if not is_professor:
                msg = "Apenas o professor da turma pode cadastrar novos projetos."
                messages.error(request, msg)
                if is_ajax:
                    return JsonResponse({"success": False, "message": msg}, status=403)
                return redirect("projetos_da_turma", turma_id=turma.idturma)

            nome_projeto = request.POST.get("nome_projeto", "").strip()
            descricao = request.POST.get("descricao", "").strip()
            imagem_file = request.FILES.get("imagem")

            if not nome_projeto:
                msg = "O nome do projeto é obrigatório."
                messages.error(request, msg)
                if is_ajax:
                    return JsonResponse({"success": False, "message": msg}, status=400)
                return redirect("projetos_da_turma", turma_id=turma.idturma)

            projeto = Projeto(
                nome_projeto=nome_projeto,
                descricao=descricao,
                turma=turma
            )
            if imagem_file:
                projeto.imagem = imagem_file

            projeto.save()

            msg = f'Projeto "{nome_projeto}" cadastrado com sucesso!'
            messages.success(request, msg)
            if is_ajax:
                return JsonResponse({"success": True, "message": msg})
            return redirect("projetos_da_turma", turma_id=turma.idturma)

        # 2. EDITAR PROJETO
        elif action == "editar_projeto":
            projeto_id = request.POST.get("projeto_id")

            try:
                projeto = Projeto.objects.get(idprojeto=projeto_id, turma=turma)
            except (Projeto.DoesNotExist, ValueError, TypeError):
                msg = "Projeto não encontrado nesta turma."
                messages.error(request, msg)
                if is_ajax:
                    return JsonResponse({"success": False, "message": msg}, status=404)
                return redirect("projetos_da_turma", turma_id=turma.idturma)

            if not (is_professor or usuario_pode_editar_projeto(usuario, projeto)):
                msg = "Você não tem permissão para editar este projeto."
                messages.error(request, msg)
                if is_ajax:
                    return JsonResponse({"success": False, "message": msg}, status=403)
                return redirect("projetos_da_turma", turma_id=turma.idturma)

            nome_novo = request.POST.get("nome_projeto", "").strip()
            if not nome_novo:
                msg = "O nome do projeto não pode ficar em branco."
                messages.error(request, msg)
                if is_ajax:
                    return JsonResponse({"success": False, "message": msg}, status=400)
                return redirect("projetos_da_turma", turma_id=turma.idturma)

            projeto.nome_projeto = nome_novo
            projeto.descricao = request.POST.get("descricao", "").strip()

            if request.FILES.get("imagem"):
                projeto.imagem = request.FILES["imagem"]

            projeto.save()

            msg = f'Projeto "{projeto.nome_projeto}" editado com sucesso!'
            messages.success(request, msg)
            if is_ajax:
                return JsonResponse({"success": True, "message": msg})
            return redirect("projetos_da_turma", turma_id=turma.idturma)

        # 3. EXCLUIR PROJETO
        elif action == "excluir_projeto":
            projeto_id = request.POST.get("projeto_id")

            try:
                projeto = Projeto.objects.get(idprojeto=projeto_id, turma=turma)
            except (Projeto.DoesNotExist, ValueError, TypeError):
                msg = "Projeto não encontrado para exclusão."
                messages.error(request, msg)
                if is_ajax:
                    return JsonResponse({"success": False, "message": msg}, status=404)
                return redirect("projetos_da_turma", turma_id=turma.idturma)

            if not is_professor:
                msg = "Apenas o professor da turma pode excluir projetos."
                messages.error(request, msg)
                if is_ajax:
                    return JsonResponse({"success": False, "message": msg}, status=403)
                return redirect("projetos_da_turma", turma_id=turma.idturma)

            nome_excluido = projeto.nome_projeto
            projeto.delete()

            msg = f'Projeto "{nome_excluido}" excluído com sucesso!'
            messages.success(request, msg)
            if is_ajax:
                return JsonResponse({"success": True, "message": msg})
            return redirect("projetos_da_turma", turma_id=turma.idturma)

        # 4. SALVAR PERMISSÕES DE ALUNOS DO PROJETO
        elif action == "salvar_alunos_repositorio":
            if not is_professor:
                msg = "Apenas o professor pode alterar as permissões dos alunos."
                messages.error(request, msg)
                if is_ajax:
                    return JsonResponse({"success": False, "message": msg}, status=403)
                return redirect("projetos_da_turma", turma_id=turma.idturma)

            projeto_id = request.POST.get("projeto_id")
            try:
                projeto = Projeto.objects.get(idprojeto=projeto_id, turma=turma)
            except (Projeto.DoesNotExist, ValueError, TypeError):
                msg = "Projeto não encontrado."
                messages.error(request, msg)
                if is_ajax:
                    return JsonResponse({"success": False, "message": msg}, status=404)
                return redirect("projetos_da_turma", turma_id=turma.idturma)

            alunos_selecionados = request.POST.getlist("alunos_edicao")
            alunos_obj = Usuario.objects.filter(idusuario__in=alunos_selecionados)
            projeto.alunos_edicao.set(alunos_obj)

            msg = f'Permissões dos alunos para o projeto "{projeto.nome_projeto}" atualizadas com sucesso!'
            messages.success(request, msg)
            if is_ajax:
                return JsonResponse({"success": True, "message": msg})
            return redirect("projetos_da_turma", turma_id=turma.idturma)

        else:
            msg = "Ação solicitada é inválida."
            messages.error(request, msg)
            if is_ajax:
                return JsonResponse({"success": False, "message": msg}, status=400)
            return redirect("projetos_da_turma", turma_id=turma.idturma)

    # GET Request
    alunos_da_turma = [ut.id_usuario for ut in turma.usuariodaturma_set.all()]

    return render(
        request,
        "AlunoProfessor/projetos.html",
        {
            "turma": turma,
            "projetos": projetos,
            "can_modify": can_modify,
            "alunos_da_turma": alunos_da_turma,
            "usuario": usuario,
        },
    )


# =========================================================================
# REPOSITÓRIO DO PROJETO (Raiz)
# =========================================================================

@require_login
def repositorio_projeto(request, projeto_id):
    """Repositório do projeto (raiz)."""
    usuario = request.usuario
    projeto = get_object_or_404(Projeto, idprojeto=projeto_id)
    can_modify = usuario_pode_editar_projeto(usuario, projeto)

    if request.method == "POST":
        if not can_modify:
            messages.error(request, "Você não tem permissão para alterar este repositório.")
            return redirect("repositorio_projeto", projeto_id=projeto.idprojeto)

        action = request.POST.get("action")

        # Criar pasta
        if action == "criar_pasta":
            nome_pasta = request.POST.get("nome_pasta", "").strip()
            if nome_pasta:
                if not Pasta.objects.filter(nome=nome_pasta, projeto=projeto, pasta_pai=None).exists():
                    Pasta.objects.create(nome=nome_pasta, criada_por=usuario, projeto=projeto)
                    messages.success(request, f'Pasta "{nome_pasta}" criada com sucesso.')
                else:
                    messages.warning(request, f'Já existe uma pasta com o nome "{nome_pasta}".')

        # Editar pasta
        elif action == "editar_pasta":
            pasta_id = request.POST.get("pasta_id")
            novo_nome = request.POST.get("novo_nome", "").strip()
            if pasta_id and novo_nome:
                pasta = get_object_or_404(Pasta, id=pasta_id, projeto=projeto)
                pasta.nome = novo_nome
                pasta.save()
                messages.success(request, "Pasta renomeada com sucesso.")

        # Excluir pasta individual
        elif action == "excluir_pasta":
            pasta_id = request.POST.get("pasta_id")
            if pasta_id:
                pasta = get_object_or_404(Pasta, id=pasta_id, projeto=projeto)
                pasta.delete()
                messages.success(request, "Pasta excluída.")

        # Excluir pastas selecionadas
        elif action == "excluir_pastas_selecionadas":
            ids = request.POST.getlist("pastas_selecionadas")
            if ids:
                Pasta.objects.filter(id__in=ids, projeto=projeto).delete()
                messages.success(request, "Pastas selecionadas excluídas.")

        # Excluir todas as pastas
        elif action == "excluir_todos_pastas":
            Pasta.objects.filter(projeto=projeto, pasta_pai=None).delete()
            messages.success(request, "Todas as pastas da raiz foram excluídas.")

        # Upload de arquivo
        elif action == "upload_arquivo":
            arquivo_file = request.FILES.get("arquivo")
            if arquivo_file:
                is_valid, error_msg = validate_file_upload(arquivo_file)
                if not is_valid:
                    messages.error(request, error_msg)
                    return redirect("repositorio_projeto", projeto_id=projeto.idprojeto)

                nome_arquivo = sanitize_filename(
                    request.POST.get("nome_arquivo") or arquivo_file.name
                )
                if not Arquivo.objects.filter(nome=nome_arquivo, projeto=projeto, pasta=None).exists():
                    pid, rtype, url = upload_para_cloudinary(
                        arquivo_file, f"projeto_{projeto.idprojeto}/{nome_arquivo}"
                    )
                    Arquivo.objects.create(
                        nome=nome_arquivo,
                        arquivo=pid,
                        resource_type=rtype,
                        enviado_por=usuario,
                        projeto=projeto,
                        url=url,
                    )
                    messages.success(request, f'Arquivo "{nome_arquivo}" enviado.')
                else:
                    messages.warning(request, f'O arquivo "{nome_arquivo}" já existe na raiz.')

        # Excluir arquivo individual
        elif action == "excluir_arquivo":
            arquivo_id = request.POST.get("arquivo_id")
            if arquivo_id:
                arquivo = get_object_or_404(Arquivo, id=arquivo_id, projeto=projeto)
                arquivo.delete()
                messages.success(request, "Arquivo excluído.")

        # Excluir arquivos selecionados
        elif action == "excluir_arquivos_selecionados":
            ids = request.POST.getlist("arquivos_selecionados")
            if ids:
                Arquivo.objects.filter(id__in=ids, projeto=projeto).delete()
                messages.success(request, "Arquivos selecionados excluídos.")

        # Excluir todos os arquivos
        elif action == "excluir_todos_arquivos":
            Arquivo.objects.filter(projeto=projeto, pasta=None).delete()
            messages.success(request, "Todos os arquivos da raiz foram excluídos.")

        # Upload de pasta completa
        elif action == "upload_pasta":
            arquivos = request.FILES.getlist("arquivos")
            enviados_count = 0
            for arquivo_file in arquivos:
                is_valid, error_msg = validate_file_upload(arquivo_file)
                if not is_valid:
                    messages.error(request, f"Arquivo '{arquivo_file.name}': {error_msg}")
                    continue

                caminho = getattr(arquivo_file, "webkitRelativePath", arquivo_file.name)
                partes = caminho.split("/")
                pasta_atual = None
                for parte in partes[:-1]:
                    pasta_atual, _ = Pasta.objects.get_or_create(
                        nome=parte,
                        projeto=projeto,
                        pasta_pai=pasta_atual,
                        defaults={"criada_por": usuario},
                    )
                nome_arquivo = sanitize_filename(partes[-1])
                if not Arquivo.objects.filter(nome=nome_arquivo, projeto=projeto, pasta=pasta_atual).exists():
                    pid, rtype, url = upload_para_cloudinary(
                        arquivo_file,
                        f"projeto_{projeto.idprojeto}/{'/'.join([sanitize_filename(p) for p in partes])}",
                    )
                    Arquivo.objects.create(
                        nome=nome_arquivo,
                        arquivo=pid,
                        resource_type=rtype,
                        enviado_por=usuario,
                        projeto=projeto,
                        pasta=pasta_atual,
                        url=url,
                    )
                    enviados_count += 1
            if enviados_count > 0:
                messages.success(request, f"{enviados_count} arquivo(s) enviado(s) com sucesso.")

        return redirect("repositorio_projeto", projeto_id=projeto.idprojeto)

    # Listagem Raiz
    pastas = Pasta.objects.filter(projeto=projeto, pasta_pai=None)
    arquivos = Arquivo.objects.filter(projeto=projeto, pasta=None)

    return render(
        request,
        "AlunoProfessor/repositorio.html",
        {
            "projeto": projeto,
            "pastas": pastas,
            "arquivos": arquivos,
            "usuario": usuario,
            "path": [],
            "can_modify": can_modify,
        },
    )


# =========================================================================
# REPOSITÓRIO DENTRO DE UMA SUBPASTA
# =========================================================================

@require_login
def repositorio_pasta(request, pasta_id):
    """Repositório dentro de uma subpasta."""
    usuario = request.usuario
    pasta_atual = get_object_or_404(Pasta, id=pasta_id)
    projeto = pasta_atual.projeto
    can_modify = usuario_pode_editar_projeto(usuario, projeto)

    # NAVEGAÇÃO BREADCRUMB
    path = []
    current = pasta_atual
    while current:
        path.insert(0, current)
        current = current.pasta_pai

    if request.method == "POST":
        if not can_modify:
            messages.error(request, "Você não tem permissão para alterar esta pasta.")
            return redirect("repositorio_pasta", pasta_id=pasta_atual.id)

        action = request.POST.get("action")

        # Criar subpasta
        if action == "criar_pasta":
            nome_pasta = request.POST.get("nome_pasta", "").strip()
            if nome_pasta:
                if not Pasta.objects.filter(nome=nome_pasta, projeto=projeto, pasta_pai=pasta_atual).exists():
                    Pasta.objects.create(
                        nome=nome_pasta,
                        criada_por=usuario,
                        projeto=projeto,
                        pasta_pai=pasta_atual,
                    )
                    messages.success(request, f'Subpasta "{nome_pasta}" criada.')
                else:
                    messages.warning(request, f'Já existe uma subpasta com o nome "{nome_pasta}".')

        # Editar subpasta
        elif action == "editar_pasta":
            subpasta_id = request.POST.get("pasta_id")
            novo_nome = request.POST.get("novo_nome", "").strip()
            if subpasta_id and novo_nome:
                subpasta = get_object_or_404(Pasta, id=subpasta_id, projeto=projeto)
                subpasta.nome = novo_nome
                subpasta.save()
                messages.success(request, "Pasta renomeada com sucesso.")

        # Excluir subpasta individual
        elif action == "excluir_pasta":
            subpasta_id = request.POST.get("pasta_id")
            if subpasta_id:
                subpasta = get_object_or_404(Pasta, id=subpasta_id, projeto=projeto)
                subpasta.delete()
                messages.success(request, "Pasta excluída.")

        # Excluir subpastas selecionadas
        elif action == "excluir_pastas_selecionadas":
            ids = request.POST.getlist("pastas_selecionadas")
            if ids:
                Pasta.objects.filter(id__in=ids, projeto=projeto).delete()
                messages.success(request, "Subpastas selecionadas excluídas.")

        # Upload de arquivo na pasta atual
        elif action == "upload_arquivo":
            arquivo_file = request.FILES.get("arquivo")
            if arquivo_file:
                is_valid, error_msg = validate_file_upload(arquivo_file)
                if not is_valid:
                    messages.error(request, error_msg)
                    return redirect("repositorio_pasta", pasta_id=pasta_atual.id)

                nome_arquivo = sanitize_filename(
                    request.POST.get("nome_arquivo") or arquivo_file.name
                )
                if not Arquivo.objects.filter(nome=nome_arquivo, projeto=projeto, pasta=pasta_atual).exists():
                    pid, rtype, url = upload_para_cloudinary(
                        arquivo_file, f"projeto_{projeto.idprojeto}/{nome_arquivo}"
                    )
                    Arquivo.objects.create(
                        nome=nome_arquivo,
                        arquivo=pid,
                        resource_type=rtype,
                        enviado_por=usuario,
                        projeto=projeto,
                        pasta=pasta_atual,
                        url=url,
                    )
                    messages.success(request, f'Arquivo "{nome_arquivo}" enviado.')
                else:
                    messages.warning(request, f'O arquivo "{nome_arquivo}" já existe nesta pasta.')

        # Upload de pasta dentro da pasta atual
        elif action == "upload_pasta":
            arquivos = request.FILES.getlist("arquivos")
            enviados_count = 0
            for arquivo_file in arquivos:
                is_valid, error_msg = validate_file_upload(arquivo_file)
                if not is_valid:
                    messages.error(request, f"Arquivo '{arquivo_file.name}': {error_msg}")
                    continue

                caminho = getattr(arquivo_file, "webkitRelativePath", arquivo_file.name)
                partes = caminho.split("/")
                pasta_corrente = pasta_atual
                for parte in partes[:-1]:
                    pasta_corrente, _ = Pasta.objects.get_or_create(
                        nome=parte,
                        projeto=projeto,
                        pasta_pai=pasta_corrente,
                        defaults={"criada_por": usuario},
                    )
                nome_arquivo = sanitize_filename(partes[-1])
                if not Arquivo.objects.filter(nome=nome_arquivo, projeto=projeto, pasta=pasta_corrente).exists():
                    pid, rtype, url = upload_para_cloudinary(
                        arquivo_file,
                        f"projeto_{projeto.idprojeto}/{'/'.join([sanitize_filename(p) for p in partes])}",
                    )
                    Arquivo.objects.create(
                        nome=nome_arquivo,
                        arquivo=pid,
                        resource_type=rtype,
                        enviado_por=usuario,
                        projeto=projeto,
                        pasta=pasta_corrente,
                        url=url,
                    )
                    enviados_count += 1
            if enviados_count > 0:
                messages.success(request, f"{enviados_count} arquivo(s) enviado(s) com sucesso.")

        # Excluir arquivo individual
        elif action == "excluir_arquivo":
            arquivo_id = request.POST.get("arquivo_id")
            if arquivo_id:
                arquivo = get_object_or_404(
                    Arquivo, id=arquivo_id, projeto=projeto, pasta=pasta_atual
                )
                arquivo.delete()
                messages.success(request, "Arquivo excluído.")

        # Excluir arquivos selecionados
        elif action == "excluir_arquivos_selecionados":
            ids = request.POST.getlist("arquivos_selecionados")
            if ids:
                Arquivo.objects.filter(id__in=ids, projeto=projeto, pasta=pasta_atual).delete()
                messages.success(request, "Arquivos selecionados excluídos.")

        return redirect("repositorio_pasta", pasta_id=pasta_atual.id)

    subpastas = Pasta.objects.filter(pasta_pai=pasta_atual)
    arquivos = Arquivo.objects.filter(pasta=pasta_atual)

    return render(
        request,
        "AlunoProfessor/repositorio.html",
        {
            "projeto": projeto,
            "pasta_atual": pasta_atual,
            "path": path,
            "pastas": subpastas,
            "arquivos": arquivos,
            "usuario": usuario,
            "can_modify": can_modify,
        },
    )


# =========================================================================
# DOWNLOAD COMPLETO DO PROJETO
# =========================================================================

@require_login
def download_repositorio_projeto(request, projeto_id):
    """Download completo do repositório como ZIP."""
    projeto = get_object_or_404(Projeto, idprojeto=projeto_id)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        adicionar_pasta_ao_zip(zip_file, projeto)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/zip")
    response["Content-Disposition"] = (
        f'attachment; filename="repositorio_projeto_{projeto.idprojeto}.zip"'
    )
    return response
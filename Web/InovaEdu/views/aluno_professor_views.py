"""
Aluno/Professor area views.
All views require authentication (checked via session).
"""
import json
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from django.contrib import messages
from django.db.models import Q

from ..models import (
    Usuario, Curso, Turma, Projeto, Forum, Topico, Mensagem,
    Eventos, Certificado, UsuarioDaTurma
)
from .utils import (
    get_usuario_from_session, require_login,
    validate_file_upload, sanitize_filename, upload_para_cloudinary,
    usuario_pode_editar_projeto, safe_redirect
)


# =========================================================================
# HOME ALUNO/PROFESSOR
# =========================================================================

@require_login
def HomeAlunoProfessor(request):
    """Home page for authenticated Aluno/Professor."""
    usuario = request.usuario

    foruns_recentes = (
        Forum.objects
        .select_related("usuario")
        .order_by("-data_criacao", "-idforum")[:4]
    )

    eventos_proximos = (
        Eventos.objects
        .filter(data_do_evento__gte=date.today())
        .order_by("data_do_evento", "hora_do_evento")[:3]
    )

    cursos_recentes = (
        Curso.objects
        .order_by("-idcurso")[:3]
    )

    context = {
        "foruns_recentes": foruns_recentes,
        "eventos_proximos": eventos_proximos,
        "cursos_recentes": cursos_recentes,
        "usuario": usuario,
    }

    return render(request, "AlunoProfessor/home.html", context)


# =========================================================================
# PERFIL
# =========================================================================

@require_login
def perfil(request):
    """Perfil do usuário logado."""
    usuario = request.usuario

    certificados = Certificado.objects.filter(usuario=usuario)

    # pegar a turma do usuário
    turma_usuario = UsuarioDaTurma.objects.filter(
        id_usuario=usuario
    ).select_related('id_turma').first()

    turma = turma_usuario.id_turma if turma_usuario else None

    # pegar projetos da turma
    projetos = Projeto.objects.filter(turma=turma) if turma else []

    return render(request, 'AlunoProfessor/perfil.html', {
        'usuario': usuario,
        'certificados': certificados,
        'projetos': projetos,
        'turma': turma
    })


@require_POST
@require_login
def atualizar_perfil_ajax(request):
    """Atualiza perfil do usuário via AJAX."""
    usuario = request.usuario

    try:
        novo_email = request.POST.get("email", "").strip()
        bio = request.POST.get("bio", "").strip()
        senha_atual = request.POST.get("senha_atual", "").strip()
        nova_senha = request.POST.get("nova_senha", "").strip()
        remover_foto = request.POST.get("remover_foto") == "true"

        # 1. Validação de campos obrigatórios
        if not novo_email:
            msg = "E-mail é obrigatório."
            messages.warning(request, msg)
            return JsonResponse({"message": msg}, status=400)

        # 2. Validação e atualização de E-mail
        if novo_email != usuario.email:
            if Usuario.objects.filter(email=novo_email).exclude(pk=usuario.pk).exists():
                msg = "Este e-mail já está em uso por outra conta."
                messages.error(request, msg)
                return JsonResponse({"message": msg}, status=400)

            usuario.email = novo_email
            request.session["usuario_email"] = novo_email

        usuario.descricao = bio

        # 3. Alteração de Senha (usando hash seguro)
        if nova_senha:
            if not usuario.check_password(senha_atual):
                msg = "Senha atual incorreta."
                messages.error(request, msg)
                return JsonResponse({"message": msg}, status=400)
            usuario.set_password(nova_senha)

        # 4. Trata a Foto de Perfil
        foto_attr = 'imagem' if hasattr(usuario, 'imagem') else 'foto'
        foto_obj = getattr(usuario, foto_attr)
        nova_foto = request.FILES.get('foto')

        # Se solicitou remover ou se enviou uma foto nova, apaga a antiga no Cloudinary
        if (remover_foto or nova_foto) and foto_obj:
            try:
                if hasattr(foto_obj, 'public_id') and foto_obj.public_id:
                    from cloudinary import uploader
                    uploader.destroy(foto_obj.public_id)
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Não foi possível deletar a imagem antiga no Cloudinary: {e}")

        if remover_foto:
            setattr(usuario, foto_attr, None)
        elif nova_foto:
            setattr(usuario, foto_attr, nova_foto)

        usuario.save()

        # Resgate da URL da foto para retorno
        foto_obj_atualizada = getattr(usuario, foto_attr)
        foto_url = foto_obj_atualizada.url if foto_obj_atualizada else "/static/img/default_user.png"

        msg = "Perfil atualizado com sucesso!"
        messages.success(request, msg)

        return JsonResponse({
            "message": msg,
            "nome": usuario.nome,
            "sobrenome": usuario.sobrenome,
            "bio": usuario.descricao,
            "foto_url": foto_url
        }, status=200)

    except Exception as e:
        msg = f"Erro interno ao atualizar perfil: {str(e)}"
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=500)


@require_POST
@require_login
def upload_foto(request):
    """Upload de foto de perfil via AJAX."""
    usuario = request.usuario

    foto = request.FILES.get("foto")

    if not foto:
        msg = "Nenhuma imagem foi enviada."
        messages.warning(request, msg)
        return JsonResponse({"message": msg}, status=400)

    try:
        foto_attr = 'imagem' if hasattr(usuario, 'imagem') else 'foto'
        setattr(usuario, foto_attr, foto)
        usuario.save()

        msg = "Foto de perfil atualizada com sucesso!"
        messages.success(request, msg)

        foto_obj = getattr(usuario, foto_attr)
        return JsonResponse({"message": msg, "foto_url": foto_obj.url}, status=200)

    except Exception as e:
        msg = f"Erro ao enviar foto: {str(e)}"
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=500)


# =========================================================================
# CURSOS E TURMAS
# =========================================================================

@require_login
def cursos(request):
    """Lista cursos disponíveis."""
    query = request.GET.get("q", "").strip()

    if query:
        curso_qs = Curso.objects.filter(nome_curso__icontains=query)
    else:
        curso_qs = Curso.objects.all()

    return render(
        request,
        "AlunoProfessor/cursos.html",
        {"curso": curso_qs, "query": query},
    )


@require_login
def turmas(request, curso_id):
    """Lista turmas de um curso."""
    curso = get_object_or_404(Curso, idcurso=curso_id)

    query = request.GET.get("q", "").strip()
    turmas_qs = Turma.objects.filter(curso=curso)

    if query:
        turmas_qs = turmas_qs.filter(codigo_turma__icontains=query)

    total_turmas = turmas_qs.count()
    turmas_qs = turmas_qs.order_by("ano")

    turmas_por_ano = {}
    for turma in turmas_qs:
        turmas_por_ano.setdefault(turma.ano, []).append(turma)

    return render(
        request,
        "AlunoProfessor/turmas.html",
        {
            "curso": curso,
            "turmas_por_ano": turmas_por_ano,
            "query": query,
            "total_turmas": total_turmas,
        },
    )


# =========================================================================
# CALENDÁRIO E EVENTOS
# =========================================================================

@require_login
def calendario(request):
    """Calendário de eventos."""
    usuario = request.usuario

    eventos = Eventos.objects.all()

    eventos_json = [
        {
            "id": evento.ideventos,
            "nome": evento.nome_do_evento,
            "data": evento.data_do_evento.strftime("%Y-%m-%d"),
            "descricao": evento.descricao,
            "hora": evento.hora_do_evento.strftime("%H:%M"),
            "endereco": evento.endereco,
            "dono_email": evento.usuario.email if evento.usuario else "Sem usuário"
        }
        for evento in eventos
    ]

    context = {
        'eventos_json': json.dumps(eventos_json),
        'usuario_email': usuario.email,
        'usuario': usuario,
    }
    return render(request, "AlunoProfessor/calendario.html", context)


@require_login
def criar_evento(request):
    """Criar novo evento."""
    usuario = request.usuario

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        data_str = request.POST.get("data")
        hora_str = request.POST.get("hora")
        descricao = request.POST.get("descricao", "").strip()
        endereco = request.POST.get("endereco", "").strip()

        if not nome or not data_str or not hora_str:
            return render(
                request,
                "AlunoProfessor/criar_evento.html",
                {
                    "erro": "Nome, data e hora são obrigatórios.",
                    "usuario": usuario,
                    "form": request.POST,
                },
            )

        try:
            from datetime import datetime
            data_do_evento = datetime.strptime(data_str, "%Y-%m-%d").date()
            hora_do_evento = datetime.strptime(hora_str, "%H:%M").time()
        except ValueError:
            return render(
                request,
                "AlunoProfessor/criar_evento.html",
                {
                    "erro": "Formato de data/hora inválido.",
                    "usuario": usuario,
                    "form": request.POST,
                },
            )

        Eventos.objects.create(
            nome_do_evento=nome,
            data_do_evento=data_do_evento,
            hora_do_evento=hora_do_evento,
            descricao=descricao,
            endereco=endereco,
            usuario=usuario,
        )
        return redirect("calendario")

    return render(request, "AlunoProfessor/criar_evento.html", {"usuario": usuario})


@require_login
def editar_evento(request, evento_id):
    """Editar evento existente."""
    usuario = request.usuario
    evento = get_object_or_404(Eventos, pk=evento_id)

    # Segurança: Se não for o dono, volta para o calendário
    if evento.usuario.email != usuario.email:
        return redirect('calendario')

    if request.method == 'POST':
        evento.nome_do_evento = request.POST.get('nome')
        evento.descricao = request.POST.get('descricao')
        evento.endereco = request.POST.get('endereco')

        data_str = request.POST.get('data')
        hora_str = request.POST.get('hora')

        if data_str and hora_str:
            from datetime import datetime
            evento.data_do_evento = datetime.strptime(data_str, '%Y-%m-%d').date()
            evento.hora_do_evento = datetime.strptime(hora_str, '%H:%M').time()

        evento.save()
        messages.success(request, "Evento atualizado com sucesso!")
        return redirect('calendario')

    return render(request, 'AlunoProfessor/editar_evento.html', {
        'evento': evento,
        'usuario': usuario
    })


@require_http_methods(["DELETE", "POST"])
@require_login
def excluir_evento(request, evento_id):
    """Excluir evento."""
    usuario = request.usuario
    evento = get_object_or_404(Eventos, pk=evento_id)

    if evento.usuario and evento.usuario.email == usuario.email:
        evento.delete()
        messages.success(request, "Evento excluído com sucesso!")
        return JsonResponse({"message": "Evento excluído com sucesso!"}, status=200)

    messages.error(request, "Você não tem permissão para excluir este evento.")
    return JsonResponse(
        {"message": "Você não tem permissão para excluir este evento."},
        status=403,
    )


# =========================================================================
# FÓRUM
# =========================================================================

@require_login
def forum_blocos(request):
    """Lista de fóruns."""
    usuario = request.usuario

    query = request.GET.get("q", "").strip()
    data_criacao = request.GET.get("data_criacao", "")
    ordenar = request.GET.get("ordenar", "")

    foruns = Forum.objects.select_related('usuario').all()

    if query:
        foruns = foruns.filter(nome__icontains=query)

    meus_foruns_count = Forum.objects.filter(usuario__email=usuario.email).count()

    if data_criacao:
        foruns = foruns.filter(data_criacao=data_criacao)

    if ordenar == "asc":
        foruns = foruns.order_by("nome")
    elif ordenar == "desc":
        foruns = foruns.order_by("-nome")

    return render(
        request,
        'AlunoProfessor/forum_blocos.html',
        {
            'foruns': foruns,
            'meus_foruns_count': meus_foruns_count,
            'query': query,
            'usuario': usuario,
        }
    )


@require_login
def criar_forum(request):
    """Criar novo fórum."""
    usuario = request.usuario

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        titulo_topico = request.POST.get("titulo_topico", "").strip()
        descricao_topico = request.POST.get("descricao_topico", "").strip()

        # Validação de segurança no backend
        meus_foruns_count = Forum.objects.filter(usuario__email=usuario.email).count()
        if meus_foruns_count >= 5:
            return redirect('forum_blocos')

        if not nome:
            messages.error(request, "Informe o nome do fórum.")
            return redirect("forum_blocos")

        forum = Forum.objects.create(
            nome=nome,
            data_criacao=date.today(),
            usuario=usuario
        )

        if titulo_topico:
            Topico.objects.create(
                forum=forum,
                titulo=titulo_topico,
                descricao=descricao_topico,
                usuario=usuario,
            )

        messages.success(request, "Fórum criado com sucesso!")
        return redirect("forum_blocos")

    return redirect("forum_blocos")


@require_login
def editar_forum(request, forum_id):
    """Editar fórum."""
    usuario = request.usuario
    forum = get_object_or_404(Forum, pk=forum_id)

    if not forum.usuario or forum.usuario.email != usuario.email:
        return redirect("forum_blocos")

    topico = forum.topicos.first()

    if request.method == "POST":
        forum_nome = request.POST.get("nome", "").strip()
        topico_titulo = request.POST.get("titulo", "").strip()
        topico_descricao = request.POST.get("descricao", "").strip()

        if forum_nome:
            forum.nome = forum_nome
            forum.save()

        if topico:
            topico.titulo = topico_titulo
            topico.descricao = topico_descricao
            topico.save()

        messages.success(request, "Fórum editado com sucesso!")
        return redirect("forum_blocos")

    return redirect("forum_blocos")


@require_login
def excluir_forum(request, forum_id):
    """Excluir fórum."""
    usuario = request.usuario

    if request.method == "POST":
        forum = get_object_or_404(Forum, pk=forum_id)

        if forum.usuario and forum.usuario.email == usuario.email:
            forum.delete()
            messages.success(request, "Fórum excluído com sucesso!")
        else:
            messages.error(request, "Você não tem permissão para excluir este fórum.")

    return redirect("forum_blocos")


@require_login
def forum_topicos(request, idforum):
    """Lista tópicos de um fórum."""
    usuario = request.usuario
    forum = get_object_or_404(Forum, idforum=idforum)

    total_meus_topicos = 0
    if usuario:
        total_meus_topicos = Topico.objects.filter(forum=forum, usuario=usuario).count()

    query = request.GET.get("q", "").strip()
    topicos = Topico.objects.filter(forum=forum)
    if query:
        topicos = topicos.filter(titulo__icontains=query)

    context = {
        "forum": forum,
        "topicos": topicos,
        "query": query,
        "total_meus_topicos": total_meus_topicos,
        "usuario": usuario,
    }
    return render(request, "AlunoProfessor/forum_topicos.html", context)


@require_login
def criar_topico(request, idforum):
    """Criar tópico em um fórum."""
    usuario = request.usuario
    forum = get_object_or_404(Forum, idforum=idforum)

    if request.method == "POST":
        total_meus_topicos = Topico.objects.filter(forum=forum, usuario=usuario).count()
        if total_meus_topicos >= 3:
            messages.error(request, "Você já atingiu o limite de 3 tópicos neste fórum.")
            return redirect("forum_topicos", idforum=forum.idforum)

        titulo = request.POST.get("titulo", "").strip()
        descricao = request.POST.get("descricao", "").strip()

        if titulo:
            Topico.objects.create(
                forum=forum, titulo=titulo, descricao=descricao, usuario=usuario
            )
            messages.success(request, "Tópico criado com sucesso!")

        return redirect("forum_topicos", idforum=forum.idforum)

    return redirect("forum_topicos", idforum=forum.idforum)


@require_login
def editar_topico(request, id):
    """Editar tópico."""
    usuario = request.usuario
    topico = get_object_or_404(Topico, idtopico=id)

    if not topico.usuario or topico.usuario.email != usuario.email:
        messages.error(request, "Você não tem permissão para editar este tópico.")
        return redirect("forum_topicos", idforum=topico.forum.idforum)

    if request.method == "POST":
        topico.titulo = request.POST.get("titulo", "").strip()
        topico.descricao = request.POST.get("descricao", "").strip()
        topico.save()
        messages.success(request, "Tópico atualizado com sucesso!")

    return redirect("forum_topicos", idforum=topico.forum.idforum)


@require_login
def excluir_topico(request, id):
    """Excluir tópico."""
    usuario = request.usuario
    topico = get_object_or_404(Topico, idtopico=id)

    if not topico.usuario or topico.usuario.email != usuario.email:
        messages.error(request, "Você não tem permissão para excluir este tópico.")
        return redirect("forum_topicos", idforum=topico.forum.idforum)

    if request.method == "POST":
        topico.delete()
        messages.success(request, "Tópico excluído com sucesso!")

    return redirect("forum_topicos", idforum=topico.forum.idforum)


@require_login
def forum_chat(request, forum_id):
    """Chat do fórum (mensagens de um tópico)."""
    usuario = request.usuario
    forum = get_object_or_404(Forum, pk=forum_id)

    topico_id = request.GET.get("topico")

    if topico_id:
        try:
            topico_selecionado = Topico.objects.get(pk=topico_id, forum=forum)
        except Topico.DoesNotExist:
            topico_selecionado = None
    else:
        topico_selecionado = forum.topicos.first()

    mensagens = []
    if topico_selecionado:
        mensagens = Mensagem.objects.filter(topico=topico_selecionado).order_by("criado_em")

    if request.method == "POST":
        conteudo = request.POST.get("conteudo")

        if topico_selecionado and conteudo and conteudo.strip():
            Mensagem.objects.create(
                topico=topico_selecionado, autor=usuario, conteudo=conteudo
            )

        return redirect(f"/forum/{forum.idforum}/?topico={topico_selecionado.pk}")

    return render(
        request,
        "AlunoProfessor/forum.html",
        {
            "forum": forum,
            "topico_selecionado": topico_selecionado,
            "mensagens": mensagens,
            "usuario": usuario,
        },
    )


@require_login
def excluir_mensagem(request, msg_id):
    """Excluir mensagem (soft delete)."""
    usuario = request.usuario
    msg = get_object_or_404(Mensagem, pk=msg_id, autor__email=usuario.email)
    msg.excluida = True
    msg.save()
    return safe_redirect(request, 'forum_blocos')


@require_login
def editar_mensagem(request, msg_id):
    """Editar mensagem (dentro de 30 min)."""
    usuario = request.usuario

    if request.method == 'POST':
        msg = get_object_or_404(Mensagem, pk=msg_id, autor__email=usuario.email)

        agora = timezone.now()
        prazo_limite = msg.criado_em + timedelta(minutes=30)

        if agora > prazo_limite:
            return safe_redirect(request, 'forum_blocos')

        novo_conteudo = request.POST.get('conteudo')
        if novo_conteudo:
            msg.conteudo = novo_conteudo
            msg.save()

    return safe_redirect(request, 'forum_blocos')


@require_GET
@require_login
def buscar_novas_mensagens(request, topico_id):
    """API: buscar novas mensagens para polling."""
    ultimo_id = request.GET.get('ultimo_id', 0)

    novas = Mensagem.objects.filter(
        topico_id=topico_id,
        id__gt=ultimo_id
    ).order_by('id')

    dados = []
    for msg in novas:
        dados.append({
            'id': msg.id,
            'autor_nome': msg.autor.nome,
            'autor_email': msg.autor.email,
            'conteudo': 'Mensagem excluída' if msg.excluida else msg.conteudo,
            'criado_em': msg.criado_em.strftime('%H:%M %d/%m/%Y'),
        })

    return JsonResponse({'mensagens': dados})
import cloudinary
from django.shortcuts import render, redirect, get_object_or_404
import resend
from datetime import date
from .models import *
import os
from datetime import datetime, timedelta
from django.utils import timezone
import json
from django.core.mail import send_mail
import random
from django.contrib import messages
import re
from cloudinary import uploader
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload as cloudinary_upload
import io
import zipfile
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator


from dotenv import load_dotenv

load_dotenv()


def login(request):
    # ele pega o que tem dentro do form
    if request.method == "GET":
        return render(request, "login.html", {"erro": "", "email": "", "senha": ""})

    #  transforma o que tinha nos inputs em dados
    Email = request.POST.get("email")
    Senha = request.POST.get("senha")

    # utiliza do usuário somente o email e a senha
    usuario = Usuario.objects.filter(email=Email, senha=Senha).first()

    # verificar se o usuario é professor aluno ou coordenador
    if usuario:
        # pegando pelo email
        request.session["usuario_email"] = usuario.email
        if usuario.tipo == "Coordenador":
            return redirect("home_Coordenacao")
        elif usuario.tipo == "Aluno" or usuario.tipo == "Professor":
            return redirect("home")
    # se ele não for, ele manda um erro e volta pro login
    else:
        return render(
            request,
            "login.html",
            {"erro": "Usuário ou senha inválidos.", "email": Email, "senha": ""},
        )


from .tokens import token_generator

def HomeAlunoProfessor(request):

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
    }

    return render(
        request,
        "AlunoProfessor/home.html",
        context
    )


# redefinir senha 
def pedir_email(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        usuario = Usuario.objects.filter(nome=nome, sobrenome=sobrenome).first()

        if usuario and usuario.email:
            # Gera o token manual
            token = token_generator.make_token(usuario)
            uid = urlsafe_base64_encode(force_bytes(usuario.idusuario))
            
            link = f"https://inova-edu.onrender.com/redefinir-senha/{uid}/{token}/"

            # Envio via Resend (mantenha sua configuração)
            resend.api_key = "re_Dn9Qt4mm_6cxkqsovJ3uhe3rWSX79rY9w"
            resend.Emails.send({
                "from": "Inova Edu <onboarding@resend.dev>",
                "to": usuario.email,
                "subject": "Redefinição de Senha",
                "html": f"<p>Link: <a href='{link}'>{link}</a></p>"
            })
            return render(request, "pedir_email.html", {"sucesso": True})
            
    return render(request, "pedir_email.html")

def redefinir_senha(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.get(idusuario=uid)
        print(f"Usuário encontrado: {usuario.nome}") # Debug
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}") # Debug
        usuario = None

    valido = token_generator.check_token(usuario, token)
    print(f"Token é válido? {valido}") # Debug

    # O check_token agora é a nossa função manual do arquivo tokens.py
    if usuario and token_generator.check_token(usuario, token):
        if request.method == 'POST':
            nova = request.POST.get('nova_senha')
            confirma = request.POST.get('confirmar_senha')

            if nova == confirma:
                usuario.senha = nova
                usuario.save()
                # Importante: após o save, o token antigo deixará de funcionar 
                # porque a senha mudou!
                return redirect('login')
            else:
                return render(request, 'redefinir_senha.html', {'erro': 'Senhas não conferem'})

        return render(request, 'redefinir_senha.html')
    else:
        return render(request, 'redefinir_senha.html', {'erro': 'Link inválido ou já utilizado.'})


# --------------- Telas aluno e professor ---------------


def cursos(request):
    query = request.GET.get("q", "").strip()

    if query:
        curso = Curso.objects.filter(nome_curso__icontains=query)
    else:
        curso = Curso.objects.all()

    return render(
        request,
        "AlunoProfessor/cursos.html",
        {
            "curso": curso,
            "query": query,
        },
    )


# perfil aluno
def perfil(request):

    email = request.session.get('usuario_email')

    if not email:
        return redirect('login')

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return redirect('login')

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
def atualizar_perfil_ajax(request):
    email_sessao = request.session.get("usuario_email")

    if not email_sessao:
        msg = "Usuário não autenticado."
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=403)

    try:
        usuario = Usuario.objects.get(email=email_sessao)
    except Usuario.DoesNotExist:
        msg = "Usuário não encontrado."
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=404)

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

        # 4. Alteração de Senha (salvando em texto puro)
        if nova_senha:
            usuario.senha = nova_senha

        # 5. Trata a Foto de Perfil
        foto_attr = 'imagem' if hasattr(usuario, 'imagem') else 'foto'
        foto_obj = getattr(usuario, foto_attr)
        nova_foto = request.FILES.get('foto')

        # Se solicitou remover ou se enviou uma foto nova, apaga a antiga no Cloudinary
        if (remover_foto or nova_foto) and foto_obj:
            try:
                if hasattr(foto_obj, 'public_id') and foto_obj.public_id:
                    cloudinary.uploader.destroy(foto_obj.public_id)
            except Exception as e:
                print(f"Aviso: Não foi possível deletar a imagem antiga no Cloudinary: {e}")

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
def upload_foto(request):
    email = request.session.get("usuario_email")

    if not email:
        msg = "Usuário não autenticado."
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=403)

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        msg = "Usuário não encontrado."
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=404)

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


def salvar_certificado(request):
    email = request.session.get("usuario_email")

    if not email:
        msg = "Usuário não autenticado."
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=403)

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        msg = "Usuário não encontrado."
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=404)

    try:
        # =========================
        # CRIAR OU EDITAR (POST)
        # =========================
        if request.method == "POST":
            data = json.loads(request.body)

            cert_id = data.get("id")
            nome = data.get("nome", "").strip()
            descricao = data.get("descricao", "").strip()
            data_inicio = data.get("data_inicio") or None
            data_final = data.get("data_final") or None

            if not nome:
                msg = "O nome do certificado é obrigatório."
                messages.warning(request, msg)
                return JsonResponse({"message": msg}, status=400)

            # EDITAR
            if cert_id:
                try:
                    certificado = Certificado.objects.get(
                        idcertificado=cert_id,
                        usuario=usuario
                    )

                    certificado.nome = nome
                    certificado.descricao = descricao
                    certificado.data_inicio = data_inicio
                    certificado.data_final = data_final
                    certificado.save()

                    msg = "Certificado atualizado com sucesso!"
                    messages.success(request, msg)
                    return JsonResponse({"message": msg}, status=200)
                
                except Certificado.DoesNotExist:
                    msg = "Certificado não encontrado."
                    messages.error(request, msg)
                    return JsonResponse({"message": msg}, status=404)

            # CRIAR
            else:
                Certificado.objects.create(
                    nome=nome,
                    descricao=descricao,
                    data_inicio=data_inicio,
                    data_final=data_final,
                    usuario=usuario
                )

                msg = "Certificado criado com sucesso!"
                messages.success(request, msg)
                return JsonResponse({"message": msg}, status=200)

        # =========================
        # EXCLUIR (DELETE)
        # =========================
        if request.method == "DELETE":
            data = json.loads(request.body)
            cert_id = data.get("id")

            try:
                certificado = Certificado.objects.get(
                    idcertificado=cert_id,
                    usuario=usuario
                )

                certificado.delete()

                msg = "Certificado excluído com sucesso!"
                messages.success(request, msg)
                return JsonResponse({"message": msg}, status=200)
            
            except Certificado.DoesNotExist:
                msg = "Certificado não encontrado."
                messages.error(request, msg)
                return JsonResponse({"message": msg}, status=404)

        msg = "Método HTTP não permitido."
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=405)

    except Exception as e:
        msg = f"Erro no processamento do certificado: {str(e)}"
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=500)


def turmas(request, curso_id):
    curso = get_object_or_404(Curso, idcurso=curso_id)

    query = request.GET.get("q", "").strip()

    turmas = Turma.objects.filter(curso=curso)

    if query:
        turmas = turmas.filter(codigo_turma__icontains=query)

    total_turmas = turmas.count()

    turmas = turmas.order_by("ano")

    turmas_por_ano = {}
    for turma in turmas:
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

from django.db.models import Q

@require_GET
def listar_projetos_ajax(request):
    """
    Retorna a lista de projetos associados ao usuário logado via JSON.
    """
    email = request.session.get("usuario_email")

    if not email:
        msg = "Usuário não autenticado."
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=403)

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        msg = "Usuário não encontrado."
        messages.error(request, msg)
        return JsonResponse({"message": msg}, status=404)

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


def projetos_da_turma(request, turma_id):
    """
    View principal para listagem, cadastro, edição, exclusão e permissões dos projetos da turma.
    """
    turma = get_object_or_404(Turma, idturma=turma_id)
    projetos = Projeto.objects.filter(turma=turma)

    # Identificação do Usuário Logado via Sessão
    email_logado = request.session.get("usuario_email")
    usuario_logado = None
    if email_logado:
        try:
            usuario_logado = Usuario.objects.get(email=email_logado)
        except Usuario.DoesNotExist:
            usuario_logado = None

    # Verifica se o usuário é o Professor da Turma
    is_professor = False
    if usuario_logado and turma.professor:
        is_professor = (usuario_logado.idusuario == turma.professor.idusuario)

    can_modify = is_professor

    # =========================================================
    # PROCESSAMENTO DE AÇÕES VIA POST
    # =========================================================
    if request.method == "POST":
        # Detecção flexível de requisição AJAX
        header_xhr = request.headers.get("x-requested-with", "") or request.headers.get("X-Requested-With", "")
        is_ajax = header_xhr.lower() == "xmlhttprequest"

        action = request.POST.get("action")

        # -----------------------------------------------------
        # 1. CADASTRAR PROJETO
        # -----------------------------------------------------
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

        # -----------------------------------------------------
        # 2. EDITAR PROJETO
        # -----------------------------------------------------
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

            # Valida se tem permissão (Se é o professor OU aluno com permissão)
            if not (is_professor or usuario_pode_editar_projeto(usuario_logado, projeto)):
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

        # -----------------------------------------------------
        # 3. EXCLUIR PROJETO
        # -----------------------------------------------------
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

        # -----------------------------------------------------
        # 4. SALVAR PERMISSÕES DE ALUNOS DO PROJETO
        # -----------------------------------------------------
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

        # -----------------------------------------------------
        # AÇÃO INVÁLIDA
        # -----------------------------------------------------
        else:
            msg = "Ação solicitada é inválida."
            messages.error(request, msg)
            if is_ajax:
                return JsonResponse({"success": False, "message": msg}, status=400)
            return redirect("projetos_da_turma", turma_id=turma.idturma)

    # GET Request: Renderização normal da página
    alunos_da_turma = [ut.id_usuario for ut in turma.usuariodaturma_set.all()]

    return render(
        request,
        "AlunoProfessor/projetos.html",
        {
            "turma": turma,
            "projetos": projetos,
            "can_modify": can_modify,
            "alunos_da_turma": alunos_da_turma,
        },
    )


# ---------- Funções Auxiliares Cloudinary e Zip ----------
def sanitize_filename(filename):
    return re.sub(r"[^A-Za-z0-9._-]", "_", filename)


def upload_para_cloudinary(arquivo_file, public_id):
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


# ---------- Download completo do projeto ----------
def download_repositorio_projeto(request, projeto_id):
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


# ---------- Repositório do projeto (Raiz) ----------
def repositorio_projeto(request, projeto_id):
    # teste de erro 500
    # raise Exception("Testando a página de erro 500!")
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")

    usuario = get_object_or_404(Usuario, email=email)
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


# ---------- Repositório dentro de uma subpasta ----------
def repositorio_pasta(request, pasta_id):
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")

    usuario = get_object_or_404(Usuario, email=email)
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


def calendario(request):
    eventos = Eventos.objects.all()
    usuario_logado_email = request.session.get('usuario_email')
    
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
        'usuario_email': usuario_logado_email # Passamos o email logado
    }
    return render(request, "AlunoProfessor/calendario.html", context)


def criar_evento(request):
    email = request.session.get('usuario_email')
    usuario = Usuario.objects.get(email=email) # Simplificado para o exemplo

    if request.method == 'POST':
        data_str = request.POST.get('data')
        data_do_evento = datetime.strptime(data_str, '%Y-%m-%d').date()

        # 🔥 REGRA: Limite de 5 eventos por dia
        eventos_hoje = Eventos.objects.filter(data_do_evento=data_do_evento).count()
        if eventos_hoje >= 5:
            messages.error(request, "Limite de 5 eventos para este dia atingido!")
            return render(request, 'AlunoProfessor/criar_evento.html', {
                'erro': 'Este dia já possui o limite máximo de 5 eventos.',
                'usuario': usuario
            })

        # ... resto do seu código de criação ...
        Eventos.objects.create(..., usuario=usuario)
        return redirect('calendario')

    return render(request, 'AlunoProfessor/criar_evento.html', {'usuario': usuario})

def editar_evento(request, evento_id):
    email = request.session.get('usuario_email')
    evento = get_object_or_404(Eventos, pk=evento_id)
    usuario = get_object_or_404(Usuario, email=email)

    # Segurança: Se não for o dono, volta para o calendário
    if evento.usuario.email != email:
        return redirect('calendario')

    if request.method == 'POST':
        # Atualiza os dados com o que veio do formulário
        evento.nome_do_evento = request.POST.get('nome')
        evento.descricao = request.POST.get('descricao')
        evento.endereco = request.POST.get('endereco')
        
        data_str = request.POST.get('data')
        hora_str = request.POST.get('hora')
        
        if data_str and hora_str:
            evento.data_do_evento = datetime.strptime(data_str, '%Y-%m-%d').date()
            evento.hora_do_evento = datetime.strptime(hora_str, '%H:%M').time()

        evento.save()
        messages.success(request, "Evento atualizado com sucesso!")
        return redirect('calendario')

    # Se for GET, renderiza a página de criação, mas com os dados do evento
    return render(request, 'AlunoProfessor/editar_evento.html', {
        'evento': evento,
        'usuario': usuario
    })

def criar_evento(request):
    email = request.session.get("usuario_email")
    usuario = None
    if email:
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            usuario = None

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        data_str = request.POST.get("data")
        hora_str = request.POST.get("hora")
        descricao = request.POST.get("descricao", "").strip()
        endereco = request.POST.get("endereco", "").strip()

        # validações básicas
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

@require_http_methods(["DELETE", "POST"])
def excluir_evento(request, evento_id):
  email = request.session.get("usuario_email")
  evento = get_object_or_404(Eventos, pk=evento_id)

  if evento.usuario and evento.usuario.email == email:
    evento.delete()
    messages.success(request, "Evento excluído com sucesso!")
    return JsonResponse({"message": "Evento excluído com sucesso!"}, status=200)

  messages.error(request, "Você não tem permissão para excluir este evento.")
  return JsonResponse(
      {"message": "Você não tem permissão para excluir este evento."},
      status=403,
  )

def forum_blocos(request):
    query = request.GET.get("q", "").strip()
    data_criacao = request.GET.get("data_criacao", "")
    ordenar = request.GET.get("ordenar", "")
    usuario_email = request.session.get('usuario_email')

    # Otimização com select_related('usuario')
    foruns = Forum.objects.select_related('usuario').all()

    if query:
        foruns = foruns.filter(nome__icontains=query)

    meus_foruns_count = Forum.objects.filter(usuario__email=usuario_email).count()

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
        }
    )

def criar_forum(request):
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return redirect("login")

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        titulo_topico = request.POST.get("titulo_topico", "").strip()
        descricao_topico = request.POST.get("descricao_topico", "").strip()

        # Validação de segurança no backend
        meus_foruns_count = Forum.objects.filter(usuario__email=email).count()
        if meus_foruns_count >= 5:
            return redirect('forum_blocos')

        # 1. Valida APENAS o nome do fórum (campo obrigatório)
        if not nome:
            messages.error(request, "Informe o nome do fórum.")
            return redirect("forum_blocos")

        # 2. Cria o Fórum
        forum = Forum.objects.create(
            nome=nome, 
            data_criacao=timezone.now().date(), 
            usuario=usuario
        )

        # 3. Cria o primeiro Tópico se preenchido
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

def editar_forum(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    email_logado = request.session.get("usuario_email")

    # Só permite editar se o usuário logado for o criador
    if not forum.usuario or email_logado != forum.usuario.email:
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


def excluir_forum(request, forum_id):
    if request.method == "POST":
        forum = get_object_or_404(Forum, pk=forum_id)
        usuario_email = request.session.get("usuario_email")

        # Só permite excluir se for o dono
        if forum.usuario and forum.usuario.email == usuario_email:
            forum.delete()
            messages.success(request, "Fórum excluído com sucesso!")
        else:
            messages.error(request, "Você não tem permissão para excluir este fórum.")

    return redirect("forum_blocos")  # volta para a página principal

def forum_topicos(request, idforum):
    forum = get_object_or_404(Forum, idforum=idforum)
    usuario_email = request.session.get("usuario_email")
    usuario = Usuario.objects.filter(email=usuario_email).first()

    # Contagem de tópicos criados pelo usuário atual neste fórum
    total_meus_topicos = 0
    if usuario:
        total_meus_topicos = Topico.objects.filter(forum=forum, usuario=usuario).count()

    # Busca de tópicos do fórum
    query = request.GET.get("q", "").strip()
    topicos = Topico.objects.filter(forum=forum)
    if query:
        topicos = topicos.filter(titulo__icontains=query)

    context = {
        "forum": forum,
        "topicos": topicos,
        "query": query,
        "total_meus_topicos": total_meus_topicos,  # Passado para o template
    }
    return render(request, "AlunoProfessor/forum_topicos.html", context)

def criar_topico(request, idforum):
    forum = get_object_or_404(Forum, idforum=idforum)
    usuario_email = request.session.get("usuario_email")
    usuario = get_object_or_404(Usuario, email=usuario_email)

    if request.method == "POST":
        # Validação do limite de 3 tópicos no servidor
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


def editar_topico(request, id):
    topico = get_object_or_404(Topico, idtopico=id)
    usuario_email = request.session.get("usuario_email")

    if not topico.usuario or topico.usuario.email != usuario_email:
        messages.error(request, "Você não tem permissão para editar este tópico.")
        return redirect("forum_topicos", idforum=topico.forum.idforum)

    if request.method == "POST":
        topico.titulo = request.POST.get("titulo", "").strip()
        topico.descricao = request.POST.get("descricao", "").strip()
        topico.save()
        messages.success(request, "Tópico atualizado com sucesso!")

    return redirect("forum_topicos", idforum=topico.forum.idforum)


def excluir_topico(request, id):
    topico = get_object_or_404(Topico, idtopico=id)
    usuario_email = request.session.get("usuario_email")

    if not topico.usuario or topico.usuario.email != usuario_email:
        messages.error(request, "Você não tem permissão para excluir este tópico.")
        return redirect("forum_topicos", idforum=topico.forum.idforum)

    if request.method == "POST":
        topico.delete()
        messages.success(request, "Tópico excluído com sucesso!")

    return redirect("forum_topicos", idforum=topico.forum.idforum)


def forum_chat(request, forum_id):
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")

    usuario = Usuario.objects.get(email=email)
    forum = Forum.objects.get(pk=forum_id)

    # Pega tópico da query string
    topico_id = request.GET.get("topico")

    if topico_id:
        try:
            topico_selecionado = Topico.objects.get(pk=topico_id, forum=forum)
        except Topico.DoesNotExist:
            topico_selecionado = None
    else:
        topico_selecionado = forum.topicos.first()

    # Só busca mensagens se existir tópico
    mensagens = []
    if topico_selecionado:
        mensagens = Mensagem.objects.filter(topico=topico_selecionado).order_by(
            "criado_em"
        )

    if request.method == "POST":
        conteudo = request.POST.get("conteudo")

        if topico_selecionado and conteudo and conteudo.strip():
            Mensagem.objects.create(
                topico=topico_selecionado, autor=usuario, conteudo=conteudo
            )

        # 🔁 mantém o tópico após enviar mensagem
        return redirect(f"/forum/{forum.idforum}/?topico={topico_selecionado.pk}")

    return render(
        request,
        "AlunoProfessor/forum.html",
        {
            "forum": forum,
            "topico_selecionado": topico_selecionado,
            "mensagens": mensagens,
        },
    )

def excluir_mensagem(request, msg_id):
    msg = get_object_or_404(Mensagem, pk=msg_id, autor__email=request.session.get('usuario_email'))
    msg.excluida = True
    msg.save()
    return redirect(request.META.get('HTTP_REFERER'))

def editar_mensagem(request, msg_id):
    if request.method == 'POST':
        msg = get_object_or_404(Mensagem, pk=msg_id, autor__email=request.session.get('usuario_email'))
        
        # Lógica dos 30 minutos
        agora = timezone.now()
        prazo_limite = msg.criado_em + timedelta(minutes=30)

        if agora > prazo_limite:
            # Opcional: enviar uma mensagem de erro (messages.error)
            return redirect(request.META.get('HTTP_REFERER'))

        novo_conteudo = request.POST.get('conteudo')
        if novo_conteudo:
            msg.conteudo = novo_conteudo
            msg.save()
            
    return redirect(request.META.get('HTTP_REFERER'))


# ================ TELAS COORDENAÇÃO ====================


def home_Coordenacao(request):
    email_sessao = request.session.get("usuario_email")

    if not email_sessao:
        return redirect("login")

    usuario_logado = get_object_or_404(Usuario, email=email_sessao)

    usuarios = Usuario.objects.all()
    cursos = Curso.objects.all()
    turmas = Turma.objects.select_related('curso').all()
    
    professores = Usuario.objects.filter(tipo__iexact="Professor")
    
  
    #dashoard total de usuários, cursos e turmas
    
    total_usuarios = usuarios.count()
    total_cursos = cursos.count()  
    total_turmas = turmas.count()
    
    
   

    if request.method == "POST":
        print(request.POST)
        acao = request.POST.get("acao")

        # EDITAR PERFIL ==========================
        if acao == "editar_perfil":
            usuario_logado.nome = request.POST.get("nome")
            usuario_logado.sobrenome = request.POST.get("sobrenome")
            usuario_logado.email = request.POST.get("email")
            usuario_logado.descricao = request.POST.get("descricao")

            if request.FILES.get("imagem"):
                usuario_logado.imagem = request.FILES.get("imagem")

            usuario_logado.save()
            return redirect("home_Coordenacao")

        #  CADASTRAR USUÁRIO ==========================

        if acao == "cadastrar_usuario":
            Usuario.objects.create(
                nome=request.POST.get("nome"),
                sobrenome=request.POST.get("sobrenome"),
                email=request.POST.get("email"),
                senha=request.POST.get("senha"),
                descricao=request.POST.get("descricao"),
                tipo=request.POST.get("tipoCadastro"),
                imagem=request.FILES.get("imagem"),
            )

            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('home_Coordenacao')
        
        

    return render(request, 'Coordenacao/home_Coordenacao.html', {
        'usuarios': usuarios,
        'professores': professores,
        'cursos': cursos,
        'turmas': turmas,
        'usuario_logado': usuario_logado,
        
        'total_usuarios': total_usuarios,
        'total_cursos': total_cursos,  
        'total_turmas': total_turmas,
    })







def listar_alunos(request):
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


def salvar_alunos_turma(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            turma_id = data.get("turma")
            alunos_ids = data.get("alunos", [])

            turma = Turma.objects.get(idturma=turma_id)

            # 🔥 remove todos vínculos antigos
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

def homePage(request):
    # Exemplo na sua view do Django:
    cursos = Curso.objects.all().order_by('-idcurso')[:3]
    return render(request, "homePage.html", {"cursos": cursos})


def excluir_usuario(request, idusuario):
    usuario = get_object_or_404(Usuario, idusuario=idusuario)
    usuario.delete()
    return redirect("home_Coordenacao")


def editar_usuario(request, idusuario):
    usuario = Usuario.objects.get(idusuario=idusuario)

    if request.method == "POST":
        # Verifica se os dados estão sendo passados corretamente
        print(request.POST)
        print(request.FILES)

        usuario.nome = request.POST.get("nome")
        usuario.sobrenome = request.POST.get("sobrenome")
        usuario.email = request.POST.get("email")
        # usuario.senha = request.POST.get("senha")
        usuario.descricao = request.POST.get("descricao")
        usuario.tipo = request.POST.get("tipoCadastro")

        if "imagem" in request.FILES:
            usuario.imagem = request.FILES["imagem"]

        usuario.save()
        print("SALVO COM SUCESSO")
        return redirect("home_Coordenacao")

    return redirect("home_Coordenacao")


# CURSO


def criar_curso(request):
    if request.method == "POST":

        email_usuario = request.session.get("usuario_email")
        if not email_usuario:
            return redirect("login")

        try:
            usuario = Usuario.objects.get(email=email_usuario)
        except Usuario.DoesNotExist:
            return redirect("login")

        Curso.objects.create(
            nome_curso=request.POST.get("nome_curso"),
            descricao_curso=request.POST.get("descricao_curso"),
            data_inicio=request.POST.get("data_inicio"),
            data_final=request.POST.get("data_final"),
            imagem=request.FILES.get("imagem"),
            usuario=usuario,
        )

        return redirect("home_Coordenacao")


def editar_curso(request):
    if request.method == "POST":
        curso = get_object_or_404(Curso, idcurso=request.POST.get("idcurso"))

        curso.nome_curso = request.POST.get("nome_curso")
        curso.data_inicio = request.POST.get("data_inicio")
        curso.data_final = request.POST.get("data_final")
        curso.descricao_curso = request.POST.get("descricao_curso")

        if request.FILES.get("imagem"):
            curso.imagem = request.FILES.get("imagem")

        curso.save()
        print("SALVO COM SUCESSO")

    # ✅ continua na mesma página
    return redirect("home_Coordenacao")


def excluir_curso(request, idcurso):
    if request.method == "POST":
        curso = get_object_or_404(Curso, idcurso=idcurso)
        curso.delete()
        return redirect(request.META.get("HTTP_REFERER", "home_Coordenacao"))


# TURMA


def criar_turma(request):
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

        return redirect("home_Coordenacao")

def editar_turma(request):
    if request.method == "POST":

        turma = get_object_or_404(
            Turma,
            idturma=request.POST.get("idturma")
        )

        turma.codigo_turma = request.POST.get("codigo_turma")
        turma.turno = request.POST.get("turno")
        turma.ano = request.POST.get("ano")
        turma.curso_id = request.POST.get("curso")

        # salvar professor
        turma.professor_id = request.POST.get("professor_id")

        turma.save()

        messages.success(request, "Editado com sucesso!")

    return redirect("home_Coordenacao")


def excluir_turma(request, idturma):
    if request.method == "POST":
        turma = get_object_or_404(Turma, idturma=idturma)
        turma.delete()
    return redirect("home_Coordenacao")


def lista_curso(request):
    cursos = Curso.objects.all()
    return render(request, 'Coordenacao/ListaCurso.html', {'cursos': cursos})
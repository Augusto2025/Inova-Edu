from django.shortcuts import render, redirect, get_object_or_404 
from .models import *
import os
from datetime import datetime
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

def login(request):
    # ele pega o que tem dentro do form
    if request.method == 'GET':
        return render(request, 'login.html', {
            'erro': '',
            'email': '',
            'senha': ''
        })

    #  transforma o que tinha nos inputs em dados
    Email = request.POST.get('email')
    Senha = request.POST.get('senha')

    # utiliza do usuário somente o email e a senha
    usuario = Usuario.objects.filter(email=Email, senha=Senha).first()

    # verificar se o usuario é professor aluno ou coordenador
    if usuario:
        # pegando pelo email
        request.session['usuario_email'] = usuario.email
        if usuario.tipo == 'Coordenador':
            return redirect('home_Coordenacao')
        elif usuario.tipo == 'Aluno' or usuario.tipo == 'Professor':
            return redirect('home')
    # se ele não for, ele manda um erro e volta pro login
    else:
        return render(request, 'login.html', {
            'erro': 'Usuário ou senha inválidos.',
            'email': Email,
            'senha': ''
        })
    
def reSenha(request):
    if request.method == "POST":
        senha1 = request.POST.get("senha1")
        senha2 = request.POST.get("senha")
        
        if senha1 == senha2:
            request.user.set_password(senha1)
            request.user.save()

    return render(request, "reSenha.html")

def pedir_email(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # Gerar código de 6 dígitos
        codigo = random.randint(100000, 999999)

        # Salvar na session
        request.session["rec_email"] = email
        request.session["rec_codigo"] = str(codigo)

        # Enviar email
        send_mail(
            subject="Código de verificação",
            message=f"Seu código é: {codigo}",
            from_email="mneto8141@gmail.com",
            recipient_list=[email],
        )

        return redirect("verificar_codigo")

    return render(request, "pedir_email.html")

def verificar_codigo(request):
    if request.method == "POST":
        codigo_digitado = request.POST.get("codigo")
        codigo_real = request.session.get("rec_codigo")

        if codigo_digitado == codigo_real:
            return redirect("redefinir_senha")

        return render(request, "verificar_codigo.html", { "erro": "Código incorreto" })

    return render(request, "verificar_codigo.html")


def redefinir_senha(request):
    if request.method == "POST":
        senha1 = request.POST.get("senha1")
        senha2 = request.POST.get("senha2")

        if senha1 != senha2:
            return render(request, "redefinir_senha.html", {
                "mensagem": "As senhas não coincidem!"
            })

        return redirect("login")

    return render(request, "redefinir_senha.html")

# --------------- Telas aluno e professor ---------------

def home(request):
    query = request.GET.get("q", "").strip()
    inicio = request.GET.get("inicio")
    fim = request.GET.get("fim")
    ordenar = request.GET.get("ordenar")

    # Pegar os eventos para usar no JavaScript
    eventos = Eventos.objects.all()
    eventos_json = [
        {
            "nome": evento.nome_do_evento,
            "data": evento.data_do_evento.strftime("%Y-%m-%d"),
            "descricao": evento.descricao,
            "hora": evento.hora_do_evento.strftime("%H:%M"),
            "endereco": evento.endereco,
        }
        for evento in eventos
    ]

    if query:
        curso = Curso.objects.filter(nome_curso__icontains=query)
    else:
        curso = Curso.objects.all()

    if inicio:
        curso = curso.filter(data_inicio__gte=inicio)

    if fim:
        curso = curso.filter(data_final__lte=fim)

    if ordenar == "asc":
        curso = curso.order_by("nome_curso")
    elif ordenar == "desc":
        curso = curso.order_by("-nome_curso")

    return render(request, 'AlunoProfessor/home.html', {
        'curso': curso,
        'query': query,
        'eventos_json': json.dumps(eventos_json),
    })


def perfil(request):
    return render(request, 'AlunoProfessor/perfil.html')

def editar_perfil(request):
    email = request.session.get('usuario_email')  # Pegando o email da sessão

    if not email:
        return redirect('login')

    # Busca pelo email em vez do ID
    usuario = get_object_or_404(Usuario, email=email)

    if request.method == "POST":
        usuario.nome = request.POST.get('nome')
        usuario.sobrenome = request.POST.get('sobrenome')
        usuario.email = request.POST.get('email')
        usuario.descricao = request.POST.get('descricao')

        if 'imagem' in request.FILES:
            usuario.imagem = request.FILES['imagem']

        usuario.save()

        # Atualiza o email se o usuário alterar
        request.session['usuario_email'] = usuario.email

        return redirect('perfil')

    return render(request, 'AlunoProfessor/editar_perfil.html', {'usuario': usuario})

def turmas(request, curso_id):
    curso = get_object_or_404(Curso, idcurso=curso_id)

    # busca turmas do curso e ordena por ano
    turmas = Turma.objects.filter(curso=curso).order_by("ano")

    # agrupar por ano
    turmas_por_ano = {}
    for turma in turmas:
        turmas_por_ano.setdefault(turma.ano, []).append(turma)

    return render(request, "AlunoProfessor/turmas.html", {
        "curso": curso,
        "turmas_por_ano": turmas_por_ano
    })


def gerenciar_alunos_projeto(request, projeto_id):
    # Pega o projeto ou 404
    projeto = get_object_or_404(Projeto, idprojeto=projeto_id)

    # Lista de todos os alunos disponíveis (pode filtrar por turma se quiser)
    alunos_disponiveis = Usuario.objects.all()

    if request.method == 'POST':
        # Pega os alunos selecionados no formulário
        selecionados = request.POST.getlist('alunos')  # lista de ids de usuários
        # Substitui os alunos do projeto pelos selecionados
        projeto.alunos.set(selecionados)
        messages.success(request, "Alunos atualizados com sucesso!")
        # Redireciona de volta para o repositório do projeto
        return redirect('repositorio_projeto', projeto_id=projeto.idprojeto)

    # Para GET, renderiza o template com os alunos atuais e disponíveis
    return render(request, 'AlunoProfessor/gerenciar_alunos.html', {
        'projeto': projeto,
        'alunos_disponiveis': alunos_disponiveis,
        'alunos_atual': projeto.alunos.all(),
    })

def api_alunos_projeto(request, projeto_id):
    """
    Retorna os dados de um projeto com os alunos disponíveis e os já cadastrados
    """
    projeto = get_object_or_404(Projeto, idprojeto=projeto_id)
    
    # Todos os alunos disponíveis (pode filtrar por turma se quiser)
    alunos_disponiveis = Usuario.objects.all()

    return JsonResponse({
        'nome_projeto': projeto.nome_projeto,
        'alunos_disponiveis': [
            {
                'id': aluno.idusuario,
                'nome': aluno.nome,
                'sobrenome': aluno.sobrenome
            } 
            for aluno in alunos_disponiveis
        ],
        'alunos_atual': [aluno.idusuario for aluno in projeto.alunos.all()]
    })

def projetos_da_turma(request, turma_id):
    # Busca a turma ou retorna 404
    turma = get_object_or_404(Turma, idturma=turma_id)
    
    # Busca todos os projetos dessa turma
    projetos = Projeto.objects.filter(turma=turma)

    return render(request, 'AlunoProfessor/projetos.html', {
        'turma': turma,
        'projetos': projetos
    })

# Função para limpar nomes de arquivos e deixar válidos para Cloudinary
def sanitize_filename(filename):
    # Substitui caracteres inválidos por _
    return re.sub(r'[^A-Za-z0-9._-]', '_', filename)

def upload_para_cloudinary(arquivo_file, public_id):
    resultado = cloudinary_upload(
        arquivo_file,
        resource_type='raw',  # para qualquer tipo de arquivo
        public_id=public_id,
        overwrite=True
    )
    
    resource_type = resultado.get('resource_type', 'raw')
    public_id_str = str(resultado['public_id'])

    url = cloudinary_url(
        public_id_str,
        resource_type=resource_type,
        version=resultado.get('version')
    )[0]

    return public_id_str, resource_type, url

def adicionar_pasta_ao_zip(zip_file, turma, pasta=None, caminho=""):
    arquivos = Arquivo.objects.filter(turma=turma, pasta=pasta)

    for arquivo in arquivos:
        r = requests.get(arquivo.url)
        zip_file.writestr(f"{caminho}{arquivo.nome}", r.content)

    subpastas = Pasta.objects.filter(turma=turma, pasta_pai=pasta)
    for subpasta in subpastas:
        adicionar_pasta_ao_zip(
            zip_file,
            turma,
            subpasta,
            f"{caminho}{subpasta.nome}/"
        )


def excluir_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, idprojeto=projeto_id)
    turma_id = projeto.turma.idturma
    projeto.delete()
    messages.success(request, "Projeto excluído com sucesso!")
    return redirect('projetos_da_turma', turma_id=turma_id)


def cadastrar_projeto(request, turma_id):
    turma = get_object_or_404(Turma, idturma=turma_id)
    if request.method == 'POST':
        nome = request.POST.get('nome_projeto')
        descricao = request.POST.get('descricao', '')

        if Projeto.objects.filter(nome_projeto=nome, turma=turma).exists():
            messages.error(request, "Já existe um projeto com esse nome nesta turma.")
        else:
            projeto = Projeto.objects.create(nome_projeto=nome, descricao=descricao, turma=turma)

            # Adicionar alunos selecionados (opcional)
            alunos_ids = request.POST.getlist('alunos')  # espera uma lista de IDs de usuários
            if alunos_ids:
                projeto.alunos.set(alunos_ids)

            messages.success(request, "Projeto cadastrado com sucesso!")
            return redirect('detalhe_turma', turma_id=turma.idturma)

    alunos = Usuario.objects.all()
    return render(request, 'AlunoProfessor/cadastrar_projeto.html', {'turma': turma, 'alunos': alunos})

def repositorio_projeto(request, projeto_id):
    email = request.session.get('usuario_email')
    if not email:
        return redirect('login')

    usuario = get_object_or_404(Usuario, email=email)
    projeto = get_object_or_404(Projeto, idprojeto=projeto_id)
    turma = projeto.turma

    # Permissão: usuário da turma pode modificar
    can_modify = UsuarioDaTurma.objects.filter(id_usuario=usuario, id_turma=turma).exists()

    if request.method == 'POST' and can_modify:
        # Criar pasta
        if 'nome_pasta' in request.POST:
            nome_pasta = request.POST.get('nome_pasta', '').strip()
            if nome_pasta:
                if Pasta.objects.filter(nome=nome_pasta, projeto=projeto, pasta_pai=None).exists():
                    messages.error(request, f"Já existe uma pasta com o nome '{nome_pasta}' neste projeto.")
                else:
                    Pasta.objects.create(nome=nome_pasta, criada_por=usuario, projeto=projeto, turma=turma)

        # Upload de arquivo
        elif 'arquivo' in request.FILES:
            arquivo_file = request.FILES['arquivo']
            if arquivo_file.size == 0:
                messages.error(request, "O arquivo enviado está vazio.")
            else:
                nome_arquivo = request.POST.get('nome_arquivo', '') or arquivo_file.name
                nome_arquivo = sanitize_filename(nome_arquivo)
                if Arquivo.objects.filter(nome=nome_arquivo, projeto=projeto, pasta=None).exists():
                    messages.error(request, f"Já existe um arquivo com o nome '{nome_arquivo}' neste projeto.")
                else:
                    public_id = f"projeto_{projeto.idprojeto}/{nome_arquivo}"
                    pid, rtype, url = upload_para_cloudinary(arquivo_file, public_id)
                    Arquivo.objects.create(
                        nome=nome_arquivo,
                        arquivo=pid,
                        resource_type=rtype,
                        enviado_por=usuario,
                        projeto=projeto,
                        turma=turma,
                        url=url
                    )

        # Upload de pasta com subpastas
        elif 'upload_pasta' in request.POST:
            arquivos = request.FILES.getlist('arquivos')
            for arquivo_file in arquivos:
                caminho = getattr(arquivo_file, 'webkitRelativePath', arquivo_file.name)
                partes = caminho.split('/')
                pasta_atual = None
                for parte in partes[:-1]:
                    pasta_atual, _ = Pasta.objects.get_or_create(
                        nome=parte,
                        projeto=projeto,
                        pasta_pai=pasta_atual,
                        criada_por=usuario,
                        turma=turma
                    )
                nome_arquivo = sanitize_filename(partes[-1])
                public_id_path = f"projeto_{projeto.idprojeto}/{'/'.join([sanitize_filename(p) for p in partes])}"
                if Arquivo.objects.filter(nome=nome_arquivo, projeto=projeto, pasta=pasta_atual).exists():
                    messages.error(request, f"Já existe um arquivo com o nome '{nome_arquivo}' na pasta de destino.")
                    continue
                pid, rtype, url = upload_para_cloudinary(arquivo_file, public_id_path)
                Arquivo.objects.create(
                    nome=nome_arquivo,
                    arquivo=pid,
                    resource_type=rtype,
                    enviado_por=usuario,
                    projeto=projeto,
                    pasta=pasta_atual,
                    turma=turma,
                    url=url
                )

        return redirect('repositorio_projeto', projeto_id=projeto.idprojeto)

    # GET
    pastas = Pasta.objects.filter(projeto=projeto, pasta_pai=None)
    arquivos = Arquivo.objects.filter(projeto=projeto, pasta=None)

    return render(request, 'AlunoProfessor/repositorio.html', {
        'projeto': projeto,
        'turma': turma,
        'pastas': pastas,
        'arquivos': arquivos,
        'usuario': usuario,
        'path': [],
        'can_modify': can_modify,
    })

def download_repositorio_projeto(request, projeto_id):
    email = request.session.get('usuario_email')
    if not email:
        return redirect('login')

    projeto = get_object_or_404(Projeto, idprojeto=projeto_id)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        adicionar_pasta_ao_zip(zip_file, projeto)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="repositorio_projeto_{projeto.idprojeto}.zip"'
    return response

def repositorio_pasta(request, pasta_id):
    email = request.session.get('usuario_email')
    if not email:
        return redirect('login')

    usuario = get_object_or_404(Usuario, email=email)
    pasta = get_object_or_404(Pasta, id=pasta_id)
    can_modify = UsuarioDaTurma.objects.filter(
        id_usuario=usuario,
        id_turma=pasta.turma
    ).exists()

    # Construir caminho (breadcrumbs)
    path = []
    current = pasta
    while current:
        path.insert(0, current)
        current = current.pasta_pai

    if request.method == 'POST' and can_modify:

        # ------------------- Criar subpasta -------------------
        if 'nome_pasta' in request.POST:
            nome_pasta = request.POST.get('nome_pasta', '').strip()
            if nome_pasta:
                if Pasta.objects.filter(
                    nome=nome_pasta,
                    turma=pasta.turma,
                    pasta_pai=pasta
                ).exists():
                    messages.error(
                        request,
                        f"Já existe uma pasta com o nome '{nome_pasta}' nesta localização."
                    )
                else:
                    Pasta.objects.create(
                        nome=nome_pasta,
                        criada_por=usuario,
                        turma=pasta.turma,
                        pasta_pai=pasta
                    )

        # ------------------- Upload de arquivo -------------------
        elif 'arquivo' in request.FILES:
            arquivo_file = request.FILES['arquivo']
            nome_arquivo = (
                request.POST.get('nome_arquivo', '').strip()
                or arquivo_file.name
            )
            nome_arquivo = sanitize_filename(nome_arquivo)

            if Arquivo.objects.filter(
                nome=nome_arquivo,
                turma=pasta.turma,
                pasta=pasta
            ).exists():
                messages.error(
                    request,
                    f"Já existe um arquivo com o nome '{nome_arquivo}' nesta localização."
                )
            else:
                public_id = f"turma_{pasta.turma.idturma}/{nome_arquivo}"
                pid, rtype, url = upload_para_cloudinary(
                    arquivo_file,
                    public_id
                )

                Arquivo.objects.create(
                    nome=nome_arquivo,
                    arquivo=pid,
                    resource_type=rtype,
                    enviado_por=usuario,
                    turma=pasta.turma,
                    pasta=pasta,
                    url=url
                )

        # ------------------- Upload de pasta (com subpastas) -------------------
        elif 'upload_pasta' in request.POST:
            arquivos = request.FILES.getlist('arquivos')

            for arquivo_file in arquivos:
                caminho = getattr(
                    arquivo_file,
                    'webkitRelativePath',
                    arquivo_file.name
                )
                partes = caminho.split('/')

                pasta_atual = pasta
                for parte in partes[:-1]:
                    subpasta, _ = Pasta.objects.get_or_create(
                        nome=parte,
                        turma=pasta.turma,
                        pasta_pai=pasta_atual,
                        criada_por=usuario
                    )
                    pasta_atual = subpasta

                nome_arquivo = sanitize_filename(partes[-1])
                public_id_path = (
                    f"turma_{pasta.turma.idturma}/"
                    f"{'/'.join([sanitize_filename(p) for p in partes])}"
                )

                if Arquivo.objects.filter(
                    nome=nome_arquivo,
                    turma=pasta.turma,
                    pasta=pasta_atual
                ).exists():
                    messages.error(
                        request,
                        f"Já existe um arquivo com o nome '{nome_arquivo}' na pasta de destino."
                    )
                    continue

                pid, rtype, url = upload_para_cloudinary(
                    arquivo_file,
                    public_id_path
                )

                Arquivo.objects.create(
                    nome=nome_arquivo,
                    arquivo=pid,
                    resource_type=rtype,
                    enviado_por=usuario,
                    turma=pasta.turma,
                    pasta=pasta_atual,
                    url=url
                )

        # ------------------- Editar subpasta -------------------
        elif 'edit_pasta' in request.POST:
            pasta_id = request.POST.get('pasta_id')
            novo_nome = request.POST.get('novo_nome', '').strip()

            subpasta = get_object_or_404(
                Pasta,
                id=pasta_id,
                pasta_pai=pasta
            )

            if subpasta.criada_por == usuario and novo_nome:
                if Pasta.objects.filter(
                    nome=novo_nome,
                    turma=pasta.turma,
                    pasta_pai=pasta
                ).exclude(id=subpasta.id).exists():
                    messages.error(
                        request,
                        f"Já existe uma pasta com o nome '{novo_nome}' nesta localização."
                    )
                else:
                    subpasta.nome = novo_nome
                    subpasta.save()

        # ------------------- Deletar arquivo -------------------
        elif 'delete_arquivo' in request.POST:
            arquivo_id = request.POST['delete_arquivo']
            arquivo = get_object_or_404(
                Arquivo,
                id=arquivo_id,
                pasta=pasta
            )
            if arquivo.enviado_por == usuario:
                arquivo.delete()

        # ------------------- Deletar arquivos selecionados -------------------
        elif 'delete_arquivos_selecionados' in request.POST:
            ids = request.POST.getlist('arquivos_selecionados')
            for arquivo_id in ids:
                arquivo = get_object_or_404(
                    Arquivo,
                    id=arquivo_id,
                    pasta=pasta
                )
                if arquivo.enviado_por == usuario:
                    arquivo.delete()

        # ------------------- Deletar subpastas selecionadas -------------------
        elif 'delete_pastas_selecionadas' in request.POST:
            ids = request.POST.getlist('pastas_selecionadas')
            for pasta_id in ids:
                subpasta = get_object_or_404(
                    Pasta,
                    id=pasta_id,
                    pasta_pai=pasta
                )
                if subpasta.criada_por == usuario:
                    subpasta.delete()

        return redirect('repositorio_pasta', pasta_id=pasta_id)

    # GET
    subpastas = Pasta.objects.filter(pasta_pai=pasta)
    arquivos = Arquivo.objects.filter(pasta=pasta)

    return render(request, 'AlunoProfessor/repositorio.html', {
        'turma': pasta.turma,
        'pasta_atual': pasta,
        'path': path,
        'pastas': subpastas,
        'arquivos': arquivos,
        'usuario': usuario,
        'can_modify': can_modify,
    })

def calendario(request):
    eventos = Eventos.objects.all()
    eventos_json = [
        {
            "nome": evento.nome_do_evento,
            "data": evento.data_do_evento.strftime("%Y-%m-%d"),
            "descricao": evento.descricao,
            "hora": evento.hora_do_evento.strftime("%H:%M"),
            "endereco": evento.endereco,
        }
        for evento in eventos
    ]
    context = {
        'eventos_json': json.dumps(eventos_json),
    }
    return render(request, 'AlunoProfessor/calendario.html', context)

def forum_blocos(request):
    query = request.GET.get("q", "").strip()
    data_criacao = request.GET.get("data_criacao", "")
    ordenar = request.GET.get("ordenar", "")

    foruns = Forum.objects.all()

    if query:
        foruns = foruns.filter(nome__icontains=query)

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
            'query': query,
        }
    )

def forum_topicos(request, idforum):
    forum = get_object_or_404(Forum, idforum=idforum)
    topicos = Topico.objects.filter(forum=forum)

    context = {
        'forum': forum,
        'topicos': topicos,
    }

    return render(request, 'AlunoProfessor/forum_topicos.html', context)


def criar_topico(request, idforum):
    forum = get_object_or_404(Forum, idforum=idforum)
    usuario_email = request.session.get('usuario_email')
    usuario = get_object_or_404(Usuario, email=usuario_email)

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        descricao = request.POST.get('descricao', '').strip()

        if titulo:
            Topico.objects.create(
                forum=forum,
                titulo=titulo,
                descricao=descricao,
                usuario=usuario
            )
            messages.success(request, "Tópico criado com sucesso!")

        return redirect('forum_topicos', idforum=forum.idforum)


def editar_topico(request, id):
    topico = get_object_or_404(Topico, idtopico=id)
    usuario_email = request.session.get('usuario_email')

    if not topico.usuario or topico.usuario.email != usuario_email:
        messages.error(request, "Você não tem permissão para editar este tópico.")
        return redirect('forum_topicos', idforum=topico.forum.idforum)

    if request.method == 'POST':
        topico.titulo = request.POST.get('titulo', '').strip()
        topico.descricao = request.POST.get('descricao', '').strip()
        topico.save()
        messages.success(request, "Tópico atualizado com sucesso!")

    return redirect('forum_topicos', idforum=topico.forum.idforum)


def excluir_topico(request, id):
    topico = get_object_or_404(Topico, idtopico=id)
    usuario_email = request.session.get('usuario_email')

    if not topico.usuario or topico.usuario.email != usuario_email:
        messages.error(request, "Você não tem permissão para excluir este tópico.")
        return redirect('forum_topicos', idforum=topico.forum.idforum)

    if request.method == "POST":
        topico.delete()
        messages.success(request, "Tópico excluído com sucesso!")

    return redirect('forum_topicos', idforum=topico.forum.idforum)


def forum_chat(request, forum_id):
    email = request.session.get('usuario_email')
    if not email:
        return redirect('login')

    usuario = Usuario.objects.get(email=email)
    forum = Forum.objects.get(pk=forum_id)

    # Pega tópico da query string
    topico_id = request.GET.get('topico')

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
        mensagens = Mensagem.objects.filter(
            topico=topico_selecionado
        ).order_by('criado_em')

    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')

        if topico_selecionado and conteudo and conteudo.strip():
            Mensagem.objects.create(
                topico=topico_selecionado,
                autor=usuario,
                conteudo=conteudo
            )

        # 🔁 mantém o tópico após enviar mensagem
        return redirect(f'/forum/{forum.idforum}/?topico={topico_selecionado.pk}')

    return render(request, 'AlunoProfessor/forum.html', {
        'forum': forum,
        'topico_selecionado': topico_selecionado,
        'mensagens': mensagens
    })


def editar_forum(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    email_logado = request.session.get('usuario_email')

    # Só permite editar se o usuário logado for o criador
    if not forum.usuario or email_logado != forum.usuario.email:
        return redirect('forum_blocos')

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

        return redirect('forum_blocos')

    return redirect('forum_blocos')

def excluir_forum(request, forum_id):
    if request.method == "POST":
        forum = get_object_or_404(Forum, pk=forum_id)
        usuario_email = request.session.get('usuario_email')

        # Só permite excluir se for o dono
        if forum.usuario and forum.usuario.email == usuario_email:
            forum.delete()
            messages.success(request, "Fórum excluído com sucesso!")
        else:
            messages.error(request, "Você não tem permissão para excluir este fórum.")

    return redirect('forum_blocos')  # volta para a página principal

def criar_forum(request):
    email = request.session.get('usuario_email')
    if not email:
        return redirect('login')

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        titulo_topico = request.POST.get('titulo_topico', '').strip()
        descricao_topico = request.POST.get('descricao_topico', '').strip()

        if not nome or not titulo_topico:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return redirect('forum_blocos')

        # 1️⃣ Cria o Fórum
        forum = Forum.objects.create(
            nome=nome,
            data_criacao=timezone.now().date(),
            usuario=usuario
        )

        # 2️⃣ Cria o primeiro Tópico
        Topico.objects.create(
            forum=forum,
            titulo=titulo_topico,
            descricao=descricao_topico,
            usuario=usuario
        )

        messages.success(request, 'Fórum criado com sucesso!')
        return redirect('forum_blocos')

    # 🚫 Não renderiza template próprio (modal cuida disso)
    return redirect('forum_blocos')

def criar_evento(request):
    email = request.session.get('usuario_email')
    usuario = None
    if email:
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            usuario = None

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        data_str = request.POST.get('data')
        hora_str = request.POST.get('hora')
        descricao = request.POST.get('descricao', '').strip()
        endereco = request.POST.get('endereco', '').strip()

        # validações básicas
        if not nome or not data_str or not hora_str:
            return render(request, 'AlunoProfessor/criar_evento.html', {
                'erro': 'Nome, data e hora são obrigatórios.',
                'usuario': usuario,
                'form': request.POST
            })

        try:
            data_do_evento = datetime.strptime(data_str, '%Y-%m-%d').date()
            hora_do_evento = datetime.strptime(hora_str, '%H:%M').time()
        except ValueError:
            return render(request, 'AlunoProfessor/criar_evento.html', {
                'erro': 'Formato de data/hora inválido.',
                'usuario': usuario,
                'form': request.POST
            })

        Eventos.objects.create(
            nome_do_evento=nome,
            data_do_evento=data_do_evento,
            hora_do_evento=hora_do_evento,
            descricao=descricao,
            endereco=endereco,
            usuario=usuario
        )
        return redirect('calendario')

    return render(request, 'AlunoProfessor/criar_evento.html', {'usuario': usuario})



# ================ TELAS COORDENAÇÃO ====================

def home_Coordenacao(request):
    email_sessao = request.session.get('usuario_email')

    if not email_sessao:
        return redirect('login')

    usuario_logado = get_object_or_404(Usuario, email=email_sessao)

    usuarios = Usuario.objects.all()
    cursos = Curso.objects.all()
    turmas = Turma.objects.select_related('curso').all()

    if request.method == 'POST':
        print(request.POST)
        acao = request.POST.get('acao')

       
        # EDITAR PERFIL ==========================
        if acao == 'editar_perfil':
            usuario_logado.nome = request.POST.get('nome')
            usuario_logado.sobrenome = request.POST.get('sobrenome')
            usuario_logado.email = request.POST.get('email')
            usuario_logado.descricao = request.POST.get('descricao')

            if request.FILES.get('imagem'):
                usuario_logado.imagem = request.FILES.get('imagem')

            usuario_logado.save()
            return redirect('home_Coordenacao')


        #  CADASTRAR USUÁRIO ==========================
       
        if acao == 'cadastrar_usuario':
            Usuario.objects.create(
                nome=request.POST.get('nome'),
                sobrenome=request.POST.get('sobrenome'),
                email=request.POST.get('email'),
                senha=request.POST.get('senha'),
                descricao=request.POST.get('descricao'),
                tipo=request.POST.get('tipoCadastro'),
                imagem=request.FILES.get('imagem')
            )

            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('home_Coordenacao')
        
        

    return render(request, 'Coordenacao/home_Coordenacao.html', {
        'usuarios': usuarios,
        'cursos': cursos,
        'turmas': turmas,
        'usuario_logado': usuario_logado,
    })




def homePage(request):
    return render(request, 'homePage.html')


def excluir_usuario(request, idusuario):
    usuario = get_object_or_404(Usuario, idusuario=idusuario)
    usuario.delete()
    return redirect('home_Coordenacao') 


def editar_usuario(request, idusuario):
    usuario = Usuario.objects.get(idusuario=idusuario)

    if request.method == "POST":
        # Verifica se os dados estão sendo passados corretamente
        print(request.POST)
        print(request.FILES)

        usuario.nome = request.POST.get("nome")
        usuario.sobrenome = request.POST.get("sobrenome")
        usuario.email = request.POST.get("email")
        usuario.senha = request.POST.get("senha")
        usuario.descricao = request.POST.get("descricao")
        usuario.tipo = request.POST.get("tipoCadastro")

        if 'imagem' in request.FILES:
            usuario.imagem = request.FILES['imagem']

        usuario.save()
        print("SALVO COM SUCESSO")
        return redirect('home_Coordenacao')

    return redirect('home_Coordenacao')




# CURSO

def criar_curso(request):
    if request.method == 'POST':

        email_usuario = request.session.get('usuario_email')
        if not email_usuario:
            return redirect('login')

        try:
            usuario = Usuario.objects.get(email=email_usuario)
        except Usuario.DoesNotExist:
            return redirect('login')

        Curso.objects.create(
            nome_curso=request.POST.get('nome_curso'),
            descricao_curso=request.POST.get('descricao_curso'),
            data_inicio=request.POST.get('data_inicio'),
            data_final=request.POST.get('data_final'),
            imagem=request.FILES.get('imagem'),
            usuario=usuario
        )

        return redirect('home_Coordenacao')

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
        return redirect(request.META.get('HTTP_REFERER', 'home_Coordenacao'))




# TURMA

def criar_turma(request):
    if request.method == 'POST':
        codigo_turma = request.POST.get('codigo_turma')
        turno = request.POST.get('turno')
        ano = request.POST.get('ano')
        curso_id = request.POST.get('curso_id')

        curso = get_object_or_404(Curso, idcurso=curso_id)

        Turma.objects.create(
            codigo_turma=codigo_turma,
            turno=turno,
            ano=ano,
            curso=curso
        )

        return redirect('home_Coordenacao')  # permanece na página



def editar_turma(request):
    if request.method == "POST":
        turma = get_object_or_404(Turma, idturma=request.POST.get('idturma'))

        turma.codigo_turma = request.POST.get('codigo_turma')
        turma.turno = request.POST.get('turno')
        turma.ano = request.POST.get('ano')
        turma.curso_id = request.POST.get('curso')

        turma.save()

        messages.success(request, "Editado com sucesso!")

    return redirect('home_Coordenacao')


def excluir_turma(request, idturma):
    if request.method == "POST":
        turma = get_object_or_404(Turma, idturma=idturma)
        turma.delete()
    return redirect('home_Coordenacao')




def lista_curso(request):
    cursos = Curso.objects.all()
    return render(request, 'Coordenacao/ListaCurso.html', {'cursos': cursos})

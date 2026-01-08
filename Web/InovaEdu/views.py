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

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'erro': '',
            'email': '',
            'senha': ''
        })

    Email = request.POST.get('email')
    Senha = request.POST.get('senha')
    usuario = Usuario.objects.filter(email=Email, senha=Senha).first()

    if usuario:
        request.session['usuario_email'] = usuario.email
        if usuario.tipo == 'Coordenador':
            return redirect('home_Coordenacao')
        elif usuario.tipo in ['Aluno', 'Professor']:
            return redirect('home')
        else:
            # caso o tipo do usuário seja algo inesperado
            messages.error(request, 'Tipo de usuário inválido.')
            return render(request, 'login.html', {'erro': 'Tipo de usuário inválido.', 'email': Email, 'senha': ''})
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

def sanitize_filename(filename):
    # Substitui caracteres inválidos por _
    return re.sub(r'[^A-Za-z0-9._-]', '_', filename)

def upload_para_cloudinary(arquivo_file, public_id):
    resultado = uploader.upload(
        arquivo_file,
        resource_type='auto',  # Cloudinary detecta automaticamente
        public_id=public_id,
        overwrite=True
    )
    # Retorna o public_id e o resource_type detectado
    resource_type = resultado.get('resource_type', 'raw')
    return resultado['public_id'], resource_type

def repositorio(request, turma_id):
    email = request.session.get('usuario_email')
    if not email:
        return redirect('login')

    usuario = get_object_or_404(Usuario, email=email)
    turma = get_object_or_404(Turma, idturma=turma_id)
    can_modify = UsuarioDaTurma.objects.filter(id_usuario=usuario, id_turma=turma).exists()

    if request.method == 'POST' and can_modify:

        # Criar nova pasta
        if 'nome_pasta' in request.POST:
            nome_pasta = request.POST.get('nome_pasta', '').strip()
            if nome_pasta:
                if Pasta.objects.filter(nome=nome_pasta, turma=turma, pasta_pai=None).exists():
                    messages.error(request, f"Já existe uma pasta com o nome '{nome_pasta}' nesta localização.")
                else:
                    Pasta.objects.create(
                        nome=nome_pasta,
                        criada_por=usuario,
                        turma=turma
                    )

        # Upload de arquivo simples
        elif 'arquivo' in request.FILES:
            arquivo_file = request.FILES['arquivo']

            if arquivo_file.size == 0:
                messages.error(request, "O arquivo enviado está vazio.")
            else:
                nome_arquivo = request.POST.get('nome_arquivo', '').strip() or arquivo_file.name
                nome_arquivo = sanitize_filename(nome_arquivo)
                if Arquivo.objects.filter(nome=nome_arquivo, turma=turma, pasta=None).exists():
                    messages.error(request, f"Já existe um arquivo com o nome '{nome_arquivo}' nesta localização.")
                else:
                    public_id = f"turma_{turma.idturma}/{nome_arquivo}"
                    pid, rtype = upload_para_cloudinary(arquivo_file, public_id)

                    Arquivo.objects.create(
                        nome=nome_arquivo,
                        arquivo=pid,
                        resource_type=rtype,
                        enviado_por=usuario,
                        turma=turma
                    )

        # Upload de múltiplos arquivos com estrutura de pastas
        elif 'upload_pasta' in request.POST:
            arquivos = request.FILES.getlist('arquivos')
            for arquivo_file in arquivos:
                if arquivo_file.size == 0:
                    messages.error(request, f"O arquivo '{arquivo_file.name}' está vazio e não foi enviado.")
                    continue

                caminho = getattr(arquivo_file, 'webkitRelativePath', arquivo_file.name)
                partes = caminho.split('/')
                pasta_atual = None
                for parte in partes[:-1]:
                    pasta, _ = Pasta.objects.get_or_create(
                        nome=parte,
                        turma=turma,
                        pasta_pai=pasta_atual,
                        criada_por=usuario
                    )
                    pasta_atual = pasta

                nome_arquivo = sanitize_filename(partes[-1])
                public_id_path = f"turma_{turma.idturma}/{'/'.join([sanitize_filename(p) for p in partes])}"
                if Arquivo.objects.filter(nome=nome_arquivo, turma=turma, pasta=pasta_atual).exists():
                    messages.error(request, f"Já existe um arquivo com o nome '{nome_arquivo}' na pasta de destino.")
                else:
                    pid, rtype = upload_para_cloudinary(arquivo_file, public_id_path)
                    Arquivo.objects.create(
                        nome=nome_arquivo,
                        arquivo=pid,
                        resource_type=rtype,
                        enviado_por=usuario,
                        turma=turma,
                        pasta=pasta_atual
                    )

        # Editar pasta
        elif 'edit_pasta' in request.POST:
            pasta_id = request.POST.get('pasta_id')
            novo_nome = request.POST.get('novo_nome', '').strip()
            pasta = get_object_or_404(Pasta, id=pasta_id, turma=turma)
            if pasta.criada_por == usuario and novo_nome:
                if Pasta.objects.filter(nome=novo_nome, turma=turma, pasta_pai=pasta.pasta_pai).exclude(id=pasta.id).exists():
                    messages.error(request, f"Já existe uma pasta com o nome '{novo_nome}' nesta localização.")
                else:
                    pasta.nome = novo_nome
                    pasta.save()

        # Deletar arquivo único
        elif 'delete_arquivo' in request.POST:
            arquivo_id = request.POST['delete_arquivo']
            arquivo = get_object_or_404(Arquivo, id=arquivo_id, turma=turma, pasta=None)
            if arquivo.enviado_por == usuario:
                arquivo.delete()

        # Deletar múltiplos arquivos
        elif 'delete_arquivos_selecionados' in request.POST:
            ids = request.POST.getlist('arquivos_selecionados')
            for arquivo_id in ids:
                arquivo = get_object_or_404(Arquivo, id=arquivo_id, turma=turma, pasta=None)
                if arquivo.enviado_por == usuario:
                    arquivo.delete()

        # Deletar pasta única
        elif 'delete_pasta' in request.POST:
            pasta_id = request.POST['delete_pasta']
            pasta = get_object_or_404(Pasta, id=pasta_id, turma=turma, pasta_pai=None)
            if pasta.criada_por == usuario:
                pasta.delete()

        # Deletar múltiplas pastas
        elif 'delete_pastas_selecionadas' in request.POST:
            ids = request.POST.getlist('pastas_selecionadas')
            for pasta_id in ids:
                pasta = get_object_or_404(Pasta, id=pasta_id, pasta_pai=None)
                if pasta.criada_por == usuario:
                    pasta.delete()

        return redirect('repositorio', turma_id=turma_id)

    # GET
    pastas = Pasta.objects.filter(turma=turma, pasta_pai=None)
    arquivos = Arquivo.objects.filter(turma=turma, pasta=None)

    return render(request, 'AlunoProfessor/repositorio.html', {
        'turma': turma,
        'pastas': pastas,
        'arquivos': arquivos,
        'usuario': usuario,
        'path': [],
        'can_modify': can_modify,
    })


def repositorio_pasta(request, pasta_id):
    email = request.session.get('usuario_email')
    if not email:
        return redirect('login')

    usuario = get_object_or_404(Usuario, email=email)
    pasta = get_object_or_404(Pasta, id=pasta_id)
    can_modify = UsuarioDaTurma.objects.filter(id_usuario=usuario, id_turma=pasta.turma).exists()

    # Construir caminho (breadcrumbs)
    path = []
    current = pasta
    while current:
        path.insert(0, current)
        current = current.pasta_pai

    if request.method == 'POST' and can_modify:

        if 'nome_pasta' in request.POST:
            nome_pasta = request.POST.get('nome_pasta', '').strip()
            if nome_pasta:
                if Pasta.objects.filter(nome=nome_pasta, turma=pasta.turma, pasta_pai=pasta).exists():
                    messages.error(request, f"Já existe uma pasta com o nome '{nome_pasta}' nesta localização.")
                else:
                    Pasta.objects.create(
                        nome=nome_pasta,
                        criada_por=usuario,
                        turma=pasta.turma,
                        pasta_pai=pasta
                    )

        elif 'arquivo' in request.FILES:
            arquivo_file = request.FILES['arquivo']
            nome_arquivo = request.POST.get('nome_arquivo', '').strip() or arquivo_file.name
            nome_arquivo = sanitize_filename(nome_arquivo)
            if Arquivo.objects.filter(nome=nome_arquivo, turma=pasta.turma, pasta=pasta).exists():
                messages.error(request, f"Já existe um arquivo com o nome '{nome_arquivo}' nesta localização.")
            else:
                public_id = f"turma_{pasta.turma.idturma}/{nome_arquivo}"
                pid, rtype = upload_para_cloudinary(arquivo_file, public_id)
                Arquivo.objects.create(
                    nome=nome_arquivo,
                    arquivo=pid,
                    resource_type=rtype,
                    enviado_por=usuario,
                    turma=pasta.turma,
                    pasta=pasta
                )

        elif 'upload_pasta' in request.POST:
            arquivos = request.FILES.getlist('arquivos')
            for arquivo_file in arquivos:
                caminho = getattr(arquivo_file, 'webkitRelativePath', arquivo_file.name)
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
                public_id_path = f"turma_{pasta.turma.idturma}/{'/'.join([sanitize_filename(p) for p in partes])}"
                if Arquivo.objects.filter(nome=nome_arquivo, turma=pasta.turma, pasta=pasta_atual).exists():
                    messages.error(request, f"Já existe um arquivo com o nome '{nome_arquivo}' na pasta de destino.")
                else:
                    pid, rtype = upload_para_cloudinary(arquivo_file, public_id_path)
                    Arquivo.objects.create(
                        nome=nome_arquivo,
                        arquivo=pid,
                        resource_type=rtype,
                        enviado_por=usuario,
                        turma=pasta.turma,
                        pasta=pasta_atual
                    )

        elif 'edit_pasta' in request.POST:
            pasta_id = request.POST.get('pasta_id')
            novo_nome = request.POST.get('novo_nome', '').strip()
            subpasta = get_object_or_404(Pasta, id=pasta_id, pasta_pai=pasta)
            if subpasta.criada_por == usuario and novo_nome:
                if Pasta.objects.filter(nome=novo_nome, turma=pasta.turma, pasta_pai=pasta).exclude(id=subpasta.id).exists():
                    messages.error(request, f"Já existe uma pasta com o nome '{novo_nome}' nesta localização.")
                else:
                    subpasta.nome = novo_nome
                    subpasta.save()

        elif 'delete_arquivo' in request.POST:
            arquivo_id = request.POST['delete_arquivo']
            arquivo = get_object_or_404(Arquivo, id=arquivo_id, pasta=pasta)
            if arquivo.enviado_por == usuario:
                arquivo.delete()

        elif 'delete_arquivos_selecionados' in request.POST:
            ids = request.POST.getlist('arquivos_selecionados')
            for arquivo_id in ids:
                arquivo = get_object_or_404(Arquivo, id=arquivo_id, pasta=pasta)
                if arquivo.enviado_por == usuario:
                    arquivo.delete()

        elif 'delete_pastas_selecionadas' in request.POST:
            ids = request.POST.getlist('pastas_selecionadas')
            for pasta_id in ids:
                subpasta = get_object_or_404(Pasta, id=pasta_id, pasta_pai=pasta)
                if subpasta.criada_por == usuario:
                    subpasta.delete()

        return redirect('repositorio_pasta', pasta_id=pasta_id)

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
        # Se não houver query string, pega o primeiro tópico do fórum
        topico_selecionado = forum.topicos.first()  # usa related_name 'topicos'

    mensagens = Mensagem.objects.filter(forum=forum).order_by('criado_em')

    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        if conteudo.strip():
            Mensagem.objects.create(
                forum=forum,
                autor=usuario,
                conteudo=conteudo
            )
        redirect_url = f'/forum/{forum.idforum}/'
        return redirect(redirect_url)

    return render(request, 'AlunoProfessor/forum.html', {
        'forum': forum,
        'topico_selecionado': topico_selecionado,
        'mensagens': mensagens
    })




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
            descricao=descricao_topico
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
                sobrenome=request.POST.get('Sobrenome'),
                email=request.POST.get('Email'),
                senha=request.POST.get('Senha'),
                descricao=request.POST.get('descricao'),
                tipo=request.POST.get('tipoCadastro'),  # OBRIGATÓRIO
                imagem=request.FILES.get('imagem')
            )
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

        # ✅ mensagem de sucesso
        messages.success(request, "Curso editado com sucesso!")

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

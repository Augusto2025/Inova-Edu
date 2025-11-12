from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from datetime import datetime
import json
from django.utils import timezone
from django.shortcuts import HttpResponse

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
    
# --------------- Telas aluno e professor ---------------

def home(request):
    # seleciona todos os campos do curso
    curso = Curso.objects.all()
    return render(request, 'AlunoProfessor/home.html', {'curso': curso})

def perfil(request):
    return render(request, 'AlunoProfessor/perfil.html')

def repositorio(request):
    return render(request, 'AlunoProfessor/repositorio.html')

def cadastro(request):
    return render(request, 'cadastro_Aluno.html')

def calendario(request):
    eventos = Eventos.objects.all()
    eventos_json = [
        {
            "nome": evento.nome_do_evento,
            "data": evento.data_do_evento.strftime("%Y-%m-%d"),
            "descricao": evento.descricao,
            "hora": evento.hora_do_evento.strftime("%H:%M"),
        }
        for evento in eventos
    ]
    context = {
        'eventos_json': json.dumps(eventos_json),
    }
    return render(request, 'AlunoProfessor/calendario.html', context)

def forum_blocos(request):
    Foruns = Forum.objects.all()
    return render(request, 'AlunoProfessor/forum_blocos.html', {'Foruns':Foruns})

def turmas(request, curso_id):
    curso = get_object_or_404(Curso, idcurso=curso_id)
    turmas = Turma.objects.filter(curso=curso)
    return render(request, 'AlunoProfessor/turmas.html', {
        'curso': curso,
        'turmas': turmas
    })

def forum_chat(request, forum_id):
    # pegar usuário logado via session
    email = request.session.get('usuario_email')
    if not email:
        return redirect('login')  # usuário não logado

    usuario = Usuario.objects.get(email=email)  # instância do usuário real

    forum = Forum.objects.get(pk=forum_id)
    mensagens = Mensagem.objects.filter(forum=forum).order_by('criado_em')

    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        if conteudo.strip():
            Mensagem.objects.create(
                forum=forum,
                autor=usuario,  # aqui passamos a instância correta
                conteudo=conteudo
            )
        return redirect('forum', forum_id=forum.idforum)

    return render(request, 'AlunoProfessor/forum.html', {'forum': forum, 'mensagens': mensagens})

def criar_forum(request):
    email = request.session.get('usuario_email')
    if not email:
        return redirect('login')

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return redirect('login')

    if usuario.tipo != 'Professor':
        return redirect('forum_blocos')

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        if nome:
            Forum.objects.create(
                nome=nome,
                data_criacao=timezone.now().date(),
                usuario=usuario
            )
            return redirect('forum_blocos')
        # se quiser, pode adicionar mensagem de erro no contexto

    return render(request, 'AlunoProfessor/criar_forum.html', {'usuario': usuario})

# --------------- Telas Coordenação ---------------

def home_Coordenacao(request):
    return render (request, 'Coordenacao/home_Coordenacao.html')

def lista_usuario(request):
    usuarios = Usuario.objects.all() #buscar todos os usuarios do banco
    return render(request, "Coordenacao/ListaUsuario.html", {'usuarios':usuarios})

def cadastroCurso(request):
    return render(request, 'Coordenacao/cadastroCurso.html')

def listacurso(request):
    return render(request, 'Coordenacao/ListaCurso.html')

def cadastroTurma(request):
    return render(request, 'Coordenacao/cadastroTurma.html')

def listaturma(request):
    return render(request, 'Coordenacao/ListaTurma.html')

def enviarUsuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('Sobrenome')
        email = request.POST.get('Email')
        senha = request.POST.get('Senha')
        descricao = request.POST.get('descricao')
        tipo = request.POST.get('tipoCadastro')
        imagem = request.FILES.get('imagem')

        # Criar e salva o usuario

        usuario = Usuario(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            senha = senha,
            descricao = descricao,
            tipo = tipo,
            imagem = imagem
        )

        usuario.save()
        
        return redirect('lista_usuario') #redireciona para pagina de listagem

    return render(request, 'Coordenacao/cadastro_usuario.html')

def excluir_usuario(request, idusuario):
    usuario = get_object_or_404(Usuario, pk=idusuario)
    usuario.delete()
    return redirect('lista_usuario')
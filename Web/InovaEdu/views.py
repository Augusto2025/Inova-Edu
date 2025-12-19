from django.shortcuts import render, redirect, get_object_or_404 
from .models import *
import os
from datetime import datetime
from django.utils import timezone
import json
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
import random


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

def repositorio(request):
    return render(request, 'AlunoProfessor/repositorio.html')


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



# --------------- TELAS COORDENAÇÃO ---------------

def home_Coordenacao(request):
    usuarios = Usuario.objects.all()
    cursos = Curso.objects.all() 
    turmas = Turma.objects.select_related('curso').all()


    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('Sobrenome')
        email = request.POST.get('Email')
        senha = request.POST.get('Senha')
        descricao = request.POST.get('descricao')
        tipo = request.POST.get('tipoCadastro')
        imagem = request.FILES.get('imagem')

        Usuario.objects.create(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            senha=senha,
            descricao=descricao,
            tipo=tipo,
            imagem=imagem
        )

        return redirect('home_Coordenacao')  # Volta para a mesma tela

    return render(request, 'Coordenacao/home_Coordenacao.html', {
        'usuarios': usuarios,
        'cursos': cursos, 
        'turmas': turmas, 
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



# EMAIL









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
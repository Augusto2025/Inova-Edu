from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
import json

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
            return redirect('cadastro_Aluno')
        elif usuario.tipo == 'Aluno' or usuario.tipo == 'Professor':
            return redirect('home')
    # se ele não for, ele manda um erro e volta pro login
    else:
        return render(request, 'login.html', {
            'erro': 'Usuário ou senha inválidos.',
            'email': Email,
            'senha': ''
        })

def home(request):
    # seleciona todos os campos do curso
    curso = Curso.objects.all()
    return render(request, 'home.html', {'curso': curso})

def perfil(request):
    return render(request, 'perfil.html')

def repositorio(request):
    return render(request, 'repositorio.html')

def cadastro(request):
    return render(request, 'cadastro_Aluno.html')

def calendario(request):
    eventos = Eventos.objects.all()
    eventos_json = [
        {
            "nome": evento.nome_do_evento,
            "data": evento.data_do_evento.strftime("%Y-%m-%d"),
        }
        for evento in eventos
    ]
    context = {
        'eventos_json': json.dumps(eventos_json)
    }
    return render(request, 'calendario.html', context)

def forum_blocos(request):
    Foruns = Forum.objects.all()
    return render(request, 'forum_blocos.html', {'Foruns':Foruns})
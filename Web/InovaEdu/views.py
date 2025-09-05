from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse

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
        elif usuario.tipo == 'Aluno':
            return redirect('home')
        elif usuario.tipo == 'Professor':
            pass
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
    return render(request, 'home_Aluno.html', {'curso': curso})

def repositorio(request):
    return render(request, 'repositorio_Aluno.html')

def perfil_A(request):
    email = request.GET.get('email')
    usuario = None
    if email:
        usuario = Usuario.objects.filter(email__iexact=email).first()
    return render(request, 'perfil_Aluno.html', {"usuario": usuario})

def cadastro_aluno(request):
    return render(request, 'cadastro_Aluno.html') 
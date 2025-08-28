from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse

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

    # verificar se o usuario é professor aluno ou coordenador
    if usuario:
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
    Curso_test = Curso.objects.all()
    return render(request, 'home_Aluno.html', {'Curso_test': Curso_test})

def cadastro_aluno(request):
    return render(request, 'cadastro_Aluno.html') 

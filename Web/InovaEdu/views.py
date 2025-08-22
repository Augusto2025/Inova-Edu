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

    if usuario:
        request.session['usuario_email'] = usuario.email
        if usuario.tipo == 'Coordenador':
            return redirect('cadastro_Aluno')  # <--- nome deve bater com urls.py
        else:
            return redirect('home')
    else:
        return render(request, 'login.html', {
            'erro': 'Usuário ou senha inválidos.',
            'email': Email,
            'senha': ''
        })

def home(request):
    return render(request, 'home_Aluno.html')

def cadastro_aluno(request):
    return render(request, 'cadastro_Aluno.html') 

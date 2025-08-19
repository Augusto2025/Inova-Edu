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
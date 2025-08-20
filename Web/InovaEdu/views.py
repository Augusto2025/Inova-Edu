from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

def set_no_cache_headers(response):
    """Evita cache completo da página"""
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'GET':
        response = render(request, 'login.html', {
            'erro': '',
            'email': '',
            'senha': ''
        })
        return set_no_cache_headers(response)
    
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    usuario = Usuario.objects.filter(email=email, senha=senha).first()

    if usuario:
        request.session['usuario_email'] = usuario.email
        response = redirect('home')
        return set_no_cache_headers(response)
    else:
        response = render(request, 'login.html', {
            'erro': 'Usuário ou senha inválidos.',
            'email': email,
            'senha': ''
        })
        return set_no_cache_headers(response)

@require_http_methods(["GET"])
def home(request):
    if not request.session.get('usuario_email'):
        response = redirect('login')
        return set_no_cache_headers(response)
    response = render(request, 'home_Aluno.html')
    return set_no_cache_headers(response)
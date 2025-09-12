from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
import calendar

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

def calendario(request, ano=None, mes=None):
    if not ano or not mes:
        hoje = datetime.today()
        ano = hoje.year
        mes = hoje.month

    eventos = Eventos.objects.filter(data_do_evento__year=ano, data_do_evento__month=mes)

    # Organiza eventos por dia
    eventos_por_dia = {}
    for evento in eventos:
        dia = evento.data_do_evento.day
        eventos_por_dia.setdefault(dia, []).append(evento)

    cal = calendar.Calendar()
    semanas_raw = cal.monthdayscalendar(ano, mes)

    semanas = []
    for semana in semanas_raw:
        semana_formatada = []
        for dia in semana:
            if dia == 0:
                # dia vazio
                semana_formatada.append({'dia': 0, 'eventos': []})
            else:
                semana_formatada.append({
                    'dia': dia,
                    'eventos': eventos_por_dia.get(dia, [])
                })
        semanas.append(semana_formatada)

    meses = list(range(1, 13))
    nomes_meses = calendar.month_name

    context = {
        'ano': ano,
        'mes': mes,
        'semanas': semanas,
        'meses': meses,
        'nomes_meses': nomes_meses,
        'eventos': eventos,
    }
    return render(request, 'calendario.html', context)
from django.shortcuts import render, redirect, get_object_or_404 
from .models import *
from datetime import datetime
from django.utils import timezone
import json
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required



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
    query = request.GET.get("q", "").strip()
    inicio = request.GET.get("inicio")
    fim = request.GET.get("fim")
    ordenar = request.GET.get("ordenar")

    if query:
        curso = Curso.objects.filter(nome_curso__icontains=query)
    else:
        curso = Curso.objects.all()

    # ---- FILTRO: data de início ----
    if inicio:
        curso = curso.filter(data_inicio__gte=inicio)

    # ---- FILTRO: data final ----
    if fim:
        curso = curso.filter(data_final__lte=fim)  # <-- CORRIGIDO

    # ---- FILTRO: ordenação ----
    if ordenar == "asc":
        curso = curso.order_by("nome_curso")
    elif ordenar == "desc":
        curso = curso.order_by("-nome_curso")

    return render(request, 'AlunoProfessor/home.html', {
        'curso': curso,
        'query': query,
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


from django.shortcuts import render, redirect
from .models import Usuario, Turma, UsuarioDaTurma, Pasta, Projeto

def repositorio(request):
    email = request.session.get('usuario_email')
    if not email:
        return redirect('login')
    
    usuario = Usuario.objects.get(email=email)
    
    turmas_usuario = Turma.objects.filter(usuariodaturma__id_usuario=usuario)
    
    repositorio_turmas = []

    for turma in turmas_usuario:
        # Pastas raiz da turma
        pastas = Pasta.objects.filter(pasta_pai=None)
        # Arquivos fora de pastas
        arquivos = Projeto.objects.filter(turma=turma, pasta=None)
        
        repositorio_turmas.append({
            'turma': turma,
            'curso': turma.curso,
            'pastas': pastas,
            'arquivos': arquivos,
        })

    return render(request, 'AlunoProfessor/repositorio.html', {'repositorio_turmas': repositorio_turmas})

def abrir_pasta(request, pasta_id):
    try:
        pasta = Pasta.objects.get(idpasta=pasta_id)
    except Pasta.DoesNotExist:
        pasta = None  # ou redirecionar para uma página de erro

    # Subpastas
    subpastas = Pasta.objects.filter(pasta_pai=pasta)

    # Arquivos dentro desta pasta
    arquivos = Projeto.objects.filter(pasta=pasta)

    # Verifica se não há subpastas ou arquivos
    sem_pastas = not subpastas.exists()
    sem_arquivos = not arquivos.exists()

    context = {
        'pasta': pasta,
        'subpastas': subpastas,
        'arquivos': arquivos,
        'sem_pastas': sem_pastas,
        'sem_arquivos': sem_arquivos,
    }

    return render(request, 'AlunoProfessor/abrir_pasta.html', context)

def criar_pasta(request, pasta_id):
    pasta_pai = Pasta.objects.get(idpasta=pasta_id)  # Pega a pasta pai

    if request.method == 'POST':
        nome_pasta = request.POST.get('nome_pasta')
        Pasta.objects.create(nome=nome_pasta, pasta_pai=pasta_pai)
        return redirect('abrir_pasta', pasta_id=pasta_id)

    return render(request, 'AlunoProfessor/criar_pasta.html', {'pasta_pai': pasta_pai})

def criar_arquivo(request, pasta_id):
    # Obter a pasta específica pelo ID
    pasta = get_object_or_404(Pasta, idpasta=pasta_id)

    if request.method == 'POST':
        # Verifique se o formulário contém o arquivo
        form = ProjetoForm(request.POST, request.FILES)  # Recebe os arquivos do formulário
        if form.is_valid():
            # Criar o projeto com o arquivo e associá-lo à pasta
            projeto = form.save(commit=False)
            projeto.pasta = pasta  # Associa o arquivo à pasta selecionada
            projeto.save()
            return redirect('abrir_pasta', pasta_id=pasta_id)  # Redireciona para a página da pasta
    else:
        # Exibe o formulário vazio
        form = ProjetoForm()

    return render(request, 'AlunoProfessor/criar_arquivo.html', {'form': form, 'pasta': pasta})

def upload_arquivo(request):
    if request.method == "POST":
        nome_projeto = request.POST.get('nome_projeto')
        arquivo = request.FILES.get('arquivo')  # Aqui pegamos o arquivo enviado

        # Cria um novo projeto e salva no banco
        projeto = Projeto.objects.create(nome_projeto=nome_projeto, arquivo=arquivo)

        # Redireciona para a página de repositório ou qualquer outra página
        return redirect('repositorio')  # ou a URL que você quiser

    return render(request, 'AlunoProfessor/upload_arquivo.html')


def cadastro(request):
    return render(request, 'Coordenacao/cadastro_Aluno.html')



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

# --------------- Telas Coordenação ---------------

def home_Coordenacao(request):
    return render (request, 'Coordenacao/home_Coordenacao.html')

def lista_usuario(request):
    usuarios = Usuario.objects.all() #buscar todos os usuarios do banco
    return render(request, "Coordenacao/ListaUsuario.html", {'usuarios':usuarios})

def cadastroCurso(request):
    return render(request, 'Coordenacao/cadastroCurso.html')

# def listacurso(request):
#     return render(request, 'Coordenacao/ListaCurso.html')

# def cadastroTurma(request):
#     return render(request, 'Coordenacao/cadastroTurma.html')

def cadastroTurma(request):
    cursos = Curso.objects.all()
    return render(request, 'Coordenacao/cadastroTurma.html', {'cursos': cursos})







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


# Turma

def enviarturma(request):
    if request.method == "POST":
        codigo_turma = request.POST.get("codigo_turma")
        turno = request.POST.get("turno")
        curso_id = request.POST.get("curso")

        curso = Curso.objects.get(idcurso=curso_id)
        
        Turma.objects.create(
            codigo_turma=codigo_turma,
            turno=turno,
            curso=curso
        )

        return redirect('listaturma')

    cursos = Curso.objects.all()
    return render(request, 'Coordenacao/cadastroTurma.html', {'cursos': cursos})


def listaturma(request):
    turmas = Turma.objects.all()
    return render(request, 'Coordenacao/ListaTurma.html', {'turmas': turmas})






# Curso


def criar_curso(request):
    if request.method == 'POST':

        # pega o email salvo na sessão na hora do login
        email_usuario = request.session.get('usuario_email')

        if not email_usuario:
            return redirect('login')  # não está logado

        # pega o usuário na sua tabela Usuario
        usuario = Usuario.objects.get(email=email_usuario)

        imagem = request.FILES.get('imagem')

        curso = Curso(
            nome_curso=request.POST['nome_curso'],
            descricao_curso=request.POST['descricao_curso'],
            data_inicio=request.POST.get('data_inicio'),
            data_final=request.POST.get('data_final'),
            usuario=usuario,
            imagem=imagem
        )

        curso.save()
        return redirect('ListaCurso')

    return render(request, 'Coordenacao/ListaCurso.html')  # GET


def lista_curso(request):
    cursos = Curso.objects.all()
    return render(request, 'Coordenacao/ListaCurso.html', {'cursos': cursos})



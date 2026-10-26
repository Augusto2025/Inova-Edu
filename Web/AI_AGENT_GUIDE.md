# Inova Edu - Guia para Agentes de IA

> **Documentação completa da arquitetura, design, segurança e padrões do sistema web Inova Edu**
> 
> **Versão:** 1.0 | **Última atualização:** 2025-01-26

---

## 📋 Índice

1. [Visão Geral do Sistema](#visão-geral-do-sistema)
2. [Arquitetura](#arquitetura)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Estrutura de Diretórios](#estrutura-de-diretórios)
5. [Modelos de Dados](#modelos-de-dados)
6. [Autenticação e Autorização](#autenticação-e-autorização)
7. [Segurança Implementada](#segurança-implementada)
8. [Principais Views e Endpoints](#principais-views-e-endpoints)
9. [Frontend e Templates](#frontend-e-templates)
10. [APIs e AJAX](#apis-e-ajax)
11. [Padrões de Código](#padrões-de-código)
12. [Configuração de Ambiente](#configuração-de-ambiente)
13. [Checklist de Segurança para Mudanças Futuras](#checklist-de-segurança-para-mudanças-futuras)

---

## 🎯 Visão Geral do Sistema

**Inova Edu** é uma plataforma educacional web desenvolvida em **Django** para gerenciamento de:
- **Projetos Integradores (PI)** - Repositórios de arquivos por turma/projeto
- **Fóruns de Discussão** - Comunicação entre alunos/professores
- **Calendário de Eventos** - Agendamento e controle de eventos
- **Certificados** - Gestão de certificados dos usuários
- **Painel de Coordenação** - Administração de usuários, cursos, turmas

### Perfis de Usuário
| Tipo | Permissões |
|------|------------|
| **Aluno** | Acessa próprios projetos, fóruns, eventos, certificados, perfil |
| **Professor** | Mesmas permissões do aluno + gerencia projetos da sua turma |
| **Coordenador** | Acesso total: CRUD de usuários, cursos, turmas, projetos |

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE (Browser)                     │
│  HTML Templates + Vanilla JS + CSS + FontAwesome            │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      DJANGO APPLICATION                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Views     │  │  Models     │  │   Templates         │  │
│  │ (Controllers)│  │  (ORM)      │  │   (DTL)             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                │                   │               │
│         └────────────────┼───────────────────┘               │
│                          ▼                                    │
│  ┌─────────────────────────────────────────────────────┐     │
│  │           MIDDLEWARE STACK (Security First)         │     │
│  │  SecurityMiddleware → WhiteNoise → Session → CSRF  │     │
│  │  → Auth → Messages → XFrameOptions → CSPMiddleware │     │
│  └─────────────────────────────────────────────────────┘     │
└────────────────────────────┬────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │ PostgreSQL │ │  Cloudinary│ │   Resend   │
       │  (Dados)   │ │  (Arquivos)│ │  (Email)   │
       └────────────┘ └────────────┘ └────────────┘
```

### Princípios Arquiteturais
1. **Fat Models, Thin Views** - Lógica de negócio nos models
2. **Security by Default** - Middleware de segurança no topo
3. **Session-based Auth** - Sem JWT, usa sessões Django seguras
4. **Role-Based Access Control (RBAC)** - Permissões por `usuario.tipo`
5. **Object-Level Permissions** - Verificação de ownership em cada view

---

## 🛠️ Stack Tecnológico

| Camada | Tecnologia | Versão |
|--------|------------|--------|
| **Framework** | Django | 6.0 |
| **Database** | PostgreSQL (prod) / MySQL (dev) | - |
| **ORM** | Django ORM | 6.0 |
| **Static Files** | WhiteNoise | 6.11 |
| **Media Storage** | Cloudinary | 1.44 |
| **Email** | Resend | 2.27 |
| **CSP** | django-csp | 4.0 |
| **Rate Limiting** | django-ratelimit | 4.1 |
| **Password Hashing** | PBKDF2 (Django built-in) | - |
| **Frontend** | Vanilla JS + CSS + FontAwesome 6 | - |
| **Deploy** | Render.com | - |

### Dependências Críticas de Segurança
```txt
django-csp==4.0          # Content Security Policy
django-ratelimit==4.1.0  # Rate limiting
whitenoise==6.11.0       # Static files com headers de segurança
```

---

## 📁 Estrutura de Diretórios

```
Web/
├── config/                    # Configurações Django
│   ├── settings.py           # ✅ Configurações de segurança completas
│   ├── urls.py               # URLConf principal
│   ├── wsgi.py / asgi.py     # Entry points
│   └── __pycache__/
├── InovaEdu/                 # App principal
│   ├── models.py             # ✅ Models com password hashing
│   ├── views.py              # ✅ Views com rate limiting, validação
│   ├── urls.py               # URLs do app
│   ├── tokens.py             # ✅ Usa Django default_token_generator
│   ├── context_processors.py # Context processor para usuario
│   ├── admin.py              # Admin vazio (custom admin não usado)
│   ├── migrations/           # Migrations do Django
│   ├── static/
│   │   ├── styles/           # CSS por funcionalidade
│   │   ├── scripts/          # JS vanilla por funcionalidade
│   │   └── img/              # Assets de imagem
│   └── templates/
│       ├── base.html         # Base template com CSP nonce
│       ├── login.html        # Login standalone
│       ├── partials/         # Partials reutilizáveis
│       ├── AlunoProfessor/   # Templates aluno/professor
│       └── Coordenacao/      # Templates coordenação
├── requirements.txt          # ✅ Dependências atualizadas
├── manage.py
├── logs/                     # Logs de segurança
│   └── security.log
├── SECURITY_AUDIT.md         # Relatório de auditoria
└── AI_AGENT_GUIDE.md         # Este arquivo
```

---

## 🗄️ Modelos de Dados

### Core Models

```python
# InovaEdu/models.py

class Usuario(models.Model):
    """Usuário customizado - NÃO usa AbstractUser"""
    idusuario = AutoField(primary_key=True)
    tipo = CharField(max_length=11)  # 'Aluno', 'Professor', 'Coordenador'
    nome = CharField(max_length=20)
    sobrenome = CharField(max_length=20)
    email = CharField(max_length=45, unique=True)
    senha = CharField(max_length=128)  # PBKDF2 hash
    descricao = CharField(max_length=100, blank=True, null=True)
    imagem = CloudinaryField(blank=True, null=True)
    
    def set_password(self, raw_password):  # ✅ Usa make_password
    def check_password(self, raw_password):  # ✅ Usa check_password
```

```python
class Curso(models.Model):
    idcurso = AutoField(primary_key=True)
    nome_curso = CharField(max_length=45)
    usuario = ForeignKey(Usuario, DO_NOTHING, null=True)  # Coordenador criador
    # ... datas, descrição, imagem
```

```python
class Turma(models.Model):
    idturma = AutoField(primary_key=True)
    codigo_turma = CharField(max_length=11)
    ano = IntegerField()
    turno = CharField(max_length=5)
    curso = ForeignKey(Curso, DO_NOTHING)
    professor = ForeignKey(Usuario, SET_NULL, null=True, related_name='turmas')
```

```python
class Projeto(models.Model):
    idprojeto = AutoField(primary_key=True)
    nome_projeto = CharField(max_length=30)
    turma = ForeignKey(Turma, DO_NOTHING)
    alunos = ManyToManyField(Usuario, related_name='projetos')
    alunos_edicao = ManyToManyField(Usuario, related_name='projetos_edicao')
    # ... descrição, imagem, datas
```

```python
class Arquivo(models.Model):
    """Arquivos no repositório do projeto"""
    nome = CharField(max_length=100)
    arquivo = CloudinaryField(resource_type='raw')
    projeto = ForeignKey(Projeto, CASCADE)
    pasta = ForeignKey('Pasta', CASCADE, null=True)
    enviado_por = ForeignKey(Usuario, CASCADE)
    url = URLField(max_length=500)  # URL direta Cloudinary
```

### Relacionamentos Importantes

```
Usuario 1──N Turma (professor)
Usuario N──N Turma (UsuarioDaTurma - alunos)
Usuario 1──N Curso (criador)
Usuario 1──N Eventos (dono)
Usuario 1──N Forum (criador)
Usuario 1──N Topico (autor)
Usuario 1──N Mensagem (autor)
Usuario 1──N Certificado (dono)
Usuario 1──N Projeto (alunos / alunos_edicao)
Usuario 1──N Arquivo (enviado_por)
Usuario 1──N Pasta (criada_por)

Turma 1──N Projeto
Projeto 1──N Pasta (hierárquica: pasta_pai)
Projeto 1──N Arquivo
Pasta 1──N Arquivo
Forum 1──N Topico
Topico 1──N Mensagem
```

---

## 🔐 Autenticação e Autorização

### Fluxo de Login
```python
# views.py - login()
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@never_cache
def login(request):
    1. GET → Render login.html
    2. POST → Busca Usuario por email (iexact)
    3. usuario.check_password(senha)  # ✅ PBKDF2 verification
    4. request.session.cycle_key()  # ✅ Session fixation prevention
    5. Seta session: usuario_email, usuario_id, usuario_tipo
    6. Redirect por tipo: Coordenador → HomeCoord, outros → home
```

### Session Management
```python
# settings.py
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600           # 1 hora
SESSION_SAVE_EVERY_REQUEST = True   # Renova a cada request
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG   # True em produção
SESSION_COOKIE_SAMESITE = 'Lax'
```

### Verificação de Permissões (Padrão)
```python
# Em todas as views protegidas:
email = request.session.get("usuario_email")
if not email:
    return redirect("login")  # ou JsonResponse 403 para AJAX

usuario = get_object_or_404(Usuario, email=email)

# Verificação de ownership:
if objeto.usuario.email != email:
    return redirect("pagina_negada")  # ou 403

# Verificação de role:
is_professor = (usuario.idusuario == turma.professor.idusuario)
can_modify = is_professor or projeto.alunos_edicao.filter(id=usuario.id).exists()
```

### Password Reset (Seguro)
```python
# tokens.py - USA DJANGO DEFAULT (HMAC + timestamp)
from django.contrib.auth.tokens import default_token_generator as token_generator

# views.py - pedir_email()
@ratelimit(key='ip', rate='3/h', method='POST', block=True)
def pedir_email(request):
    token = token_generator.make_token(usuario)  # ✅ Seguro
    uid = urlsafe_base64_encode(force_bytes(usuario.idusuario))
    link = f"https://inova-edu.onrender.com/redefinir-senha/{uid}/{token}/"
    # Envia via Resend (API key em env var)

# views.py - redefinir_senha()
@ratelimit(key='ip', rate='5/h', method='POST', block=True)
def redefinir_senha(request, uidb64, token):
    if token_generator.check_token(usuario, token):  # ✅ Valida HMAC
        usuario.set_password(nova_senha)  # ✅ Hash novo
        usuario.save()  # Token invalida automaticamente (password mudou)
```

---

## 🛡️ Segurança Implementada

### 1. Password Security ✅
- **PBKDF2 com SHA-256** (Django default, 600k iterações)
- `set_password()` / `check_password()` em `Usuario` model
- NUNCA armazena senha em texto puro

### 2. CSRF Protection ✅
- `CsrfViewMiddleware` ativo
- `@csrf_exempt` REMOVIDO de todas as views
- Templates usam `{% csrf_token %}`
- AJAX envia header `X-CSRFToken`
- View customizada `csrf_failure` para 403 amigável

### 3. Content Security Policy ✅
```python
# settings.py
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)           # Sem 'unsafe-inline'!
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://cdnjs.cloudflare.com", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "https://res.cloudinary.com")
CSP_INCLUDE_NONCE_IN = ['script-src', 'style-src']
```
- Nonce automático em `<script nonce="{{ request.csp_nonce }}">`
- External fonts/CDNs permitidos explicitamente

### 4. Security Headers ✅
```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000 (produção)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
XFrameOptionsMiddleware → DENY
```

### 5. Cookies Seguros ✅
```python
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'Lax'
```

### 6. Rate Limiting ✅
```python
# Login: 5 req/min por IP
@ratelimit(key='ip', rate='5/m', method='POST', block=True)

# Password reset request: 3 req/hora por IP
@ratelimit(key='ip', rate='3/h', method='POST', block=True)

# Password reset confirm: 5 req/hora por IP
@ratelimit(key='ip', rate='5/h', method='POST', block=True)
```

### 7. File Upload Validation ✅
```python
# views.py - validate_file_upload()
ALLOWED_FILE_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.py', '.js', '.jpg', '.png', ...}
BLOCKED_MIME_TYPES = {'application/x-msdownload', 'application/x-php', ...}
MAX_FILE_SIZE = 10 MB

# Aplicado em TODOS upload_arquivo e upload_pasta
```

### 8. Open Redirect Prevention ✅
```python
# views.py - safe_redirect()
def safe_redirect(request, fallback_url_name):
    referer = request.META.get('HTTP_REFERER')
    if referer and urlparse(referer).netloc == urlparse(request.build_absolute_uri('/')).netloc:
        return redirect(referer)
    return redirect(fallback_url_name)
```

### 9. Session Fixation Prevention ✅
```python
request.session.cycle_key()  # No login bem-sucedido
```

### 10. SQL Injection Prevention ✅
- **Apenas Django ORM** - Zero raw SQL
- `filter()`, `get()`, `exclude()` com parâmetros seguros

### 11. XSS Prevention ✅
- Templates Django auto-escaping (padrão)
- CSP bloqueia inline scripts sem nonce
- `|escapejs` usado em JSON para JS

### 12. Secrets Management ✅
```python
# Tudo em variáveis de ambiente (.env)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
CLOUDINARY_* = os.environ.get(...)
DATABASE_URL = os.environ.get('DATABASE_URL')
```
- **ZERO secrets hardcoded** no código

### 13. Logging de Segurança ✅
```python
# settings.py - LOGGING
'django.security': WARNING → console + security.log
'django.request': ERROR → console + security.log
'InovaEdu': INFO → console + security.log
```

---

## 🔗 Principais Views e Endpoints

### Públicas (Sem Auth)
| URL | View | Método | Descrição |
|-----|------|--------|-----------|
| `/` | `homePage` | GET | Landing page |
| `/login/` | `login` | GET/POST | Login com rate limit |
| `/pedir_email/` | `pedir_email` | GET/POST | Solicitar reset senha |
| `/redefinir-senha/<uid>/<token>/` | `redefinir_senha` | GET/POST | Confirmar reset |

### Aluno/Professor (Requer Auth + Tipo Aluno/Professor)
| URL | View | Método | Descrição |
|-----|------|--------|-----------|
| `/home/` | `HomeAlunoProfessor` | GET | Dashboard |
| `/cursos/` | `cursos` | GET | Lista cursos |
| `/perfil/` | `perfil` | GET | Perfil do usuário |
| `/api/atualizar-perfil/` | `atualizar_perfil_ajax` | POST | Atualiza perfil/senha/foto |
| `/api/upload-foto/` | `upload_foto` | POST | Upload foto perfil |
| `/api/certificados/` | `salvar_certificado` | POST/DELETE | CRUD certificados |
| `/calendario/` | `calendario` | GET | Calendário eventos |
| `/calendario/criar/` | `criar_evento` | GET/POST | Criar evento (limite 5/dia) |
| `/calendario/editar/<id>/` | `editar_evento` | GET/POST | Editar próprio evento |
| `/calendario/excluir/<id>/` | `excluir_evento` | DELETE/POST | Excluir próprio evento |
| `/forum_blocos/` | `forum_blocos` | GET | Lista fóruns |
| `/forum/<id>/` | `forum_chat` | GET/POST | Chat do fórum |
| `/forum/criar/` | `criar_forum` | POST | Criar fórum (limite 5/user) |
| `/curso/<id>/turmas/` | `turmas` | GET | Turmas do curso |
| `/turma/<id>/projetos/` | `projetos_da_turma` | GET/POST | Projetos da turma |
| `/projeto/<id>/repositorio/` | `repositorio_projeto` | GET/POST | Repositório raiz |
| `/repositorio/pasta/<id>/` | `repositorio_pasta` | GET/POST | Subpasta |
| `/repositorio/<id>/download/` | `download_repositorio_projeto` | GET | Download ZIP |

### Coordenação (Requer Auth + Tipo Coordenador)
| URL | View | Método | Descrição |
|-----|------|--------|-----------|
| `/coordenacao/` | `HomeCoord` | GET | Dashboard admin |
| `/usuarios/` | `UsuarioCoord` | GET/POST | CRUD usuários |
| `/CursoCoord/` | `CursoCoord` | GET | Lista cursos |
| `/criar_curso/` | `criar_curso` | POST | Criar curso |
| `/curso/editar/` | `editar_curso` | POST | Editar curso |
| `/curso/excluir/<id>/` | `excluir_curso` | POST | Excluir curso |
| `/TurmaCoord/` | `TurmaCoord` | GET | Lista turmas |
| `/criar_turma/` | `criar_turma` | POST | Criar turma |
| `/turma/editar/` | `editar_turma` | POST | Editar turma |
| `/turma/excluir/<id>/` | `excluir_turma` | POST | Excluir turma |
| `/turma/listar-alunos/<id>/` | `listar_alunos_turma` | GET | Alunos da turma (JSON) |
| `/turma/salvar-alunos/` | `salvar_turma_usuario` | POST | Vincular alunos à turma |
| `/projetosCoord/` | `projetosCoord` | GET | Todos projetos |

---

## 🎨 Frontend e Templates

### Base Template (`base.html`)
- CSP nonce em `<link>` e `<script>`
- Estrutura: `header` → `content` → `footer` → `chat` → `menssagem`
- Script global para desabilitar botões submit duplicados
- BFCache fix para botões "Voltar" do navegador

### Partials Reutilizáveis
| Partial | Descrição |
|---------|-----------|
| `partials/header.html` | Navbar aluno/professor com menu mobile |
| `partials/navbar_Coordenacao.html` | Navbar coordenação |
| `partials/footer.html` | Footer simples |
| `partials/menssagem.html` | Exibe `messages` framework |
| `partials/chatbot.html` | Chatbot estático (localStorage) |

### JavaScript Vanilla (Sem Framework)
| Script | Funcionalidade |
|--------|----------------|
| `scripts/perfil.js` | Modal perfil, certificados, foto, AJAX |
| `scripts/chat_suporte.js` | Chatbot FAQ localStorage |
| `scripts/buscageral.js` | Busca geral (vazio) |
| `scripts/home_coordenacao.js` | Dashboard coordenação |
| `scripts/modal_descricao.js` | Modais de descrição |
| `scripts/salvar_senha.js` | (Vazio) |

### Padrões Frontend
- **Modais** em HTML no template, controlados por JS (`display: flex`)
- **AJAX** com `fetch()` + `FormData` ou `JSON`
- **CSRF Token** via `<input type="hidden" id="csrf-token" value="{{ csrf_token }}">`
- **Feedback** via toast notifications customizadas
- **Loading** overlay global

---

## 📡 APIs e AJAX

### Endpoints AJAX Principais

```javascript
// Headers padrão
const headers = {
    'X-CSRFToken': csrftoken,
    'Content-Type': 'application/json',
};

// Atualizar perfil (multipart/form-data para foto)
await fetch('/api/atualizar-perfil/', {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    body: formData  // FormData para upload de arquivo
});

// Certificados (JSON)
await fetch('/api/certificados/', {
    method: 'POST',  // ou DELETE
    headers: headers,
    body: JSON.stringify({ id, nome, descricao, data_inicio, data_final })
});

// Upload foto perfil
await fetch('/api/upload-foto/', {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    body: formData
});

// Listar projetos do usuário
const response = await fetch('/api/listar-projetos/', {
    headers: { 'X-CSRFToken': csrftoken }
});
const { projetos } = await response.json();
```

### Respostas Padronizadas
```json
// Sucesso
{ "message": "Perfil atualizado com sucesso!", "nome": "...", "foto_url": "..." }

// Erro
{ "message": "Erro descritivo", "status": 400|403|404|500 }
```

---

## 📝 Padrões de Código

### Views - Estrutura Padrão
```python
@require_http_methods(["GET", "POST"])  # Ou @require_POST, @require_GET
@ratelimit(key='ip', rate='X/m', method='POST', block=True)  # Se sensível
@never_cache  # Se manipula estado
def minha_view(request):
    # 1. Autenticação
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")  # ou JsonResponse 403
    
    usuario = get_object_or_404(Usuario, email=email)
    
    # 2. Autorização (se necessário)
    if not usuario_pode_editar_projeto(usuario, projeto):
        return JsonResponse({"message": "Sem permissão"}, status=403)
    
    # 3. GET → Render
    if request.method == "GET":
        return render(request, "template.html", context)
    
    # 4. POST → Processar
    try:
        # Validação de entrada
        # Lógica de negócio
        # Save com tratamento de erro
        return JsonResponse({"message": "Sucesso"}, status=200)
    except Exception as e:
        logger.error(f"Erro em minha_view: {e}")
        return JsonResponse({"message": "Erro interno"}, status=500)
```

### Tratamento de Erros
- **Try/Except** em toda lógica POST
- **Logging** com `logger.error/warning/info`
- **Mensagens user-friendly** (sem stack trace)
- **Status codes** HTTP corretos

### Validação de Entrada
```python
# Sempre validar:
nome = request.POST.get("nome", "").strip()
if not nome:
    return JsonResponse({"message": "Nome obrigatório"}, status=400)

# Para IDs:
projeto_id = request.POST.get("projeto_id")
try:
    projeto = Projeto.objects.get(idprojeto=projeto_id, turma=turma)
except (Projeto.DoesNotExist, ValueError, TypeError):
    return JsonResponse({"message": "Projeto inválido"}, status=404)
```

### Queries Otimizadas
```python
# select_related para FK (1 query)
foruns = Forum.objects.select_related("usuario").all()

# prefetch_related para M2M/reverse FK
projetos = Projeto.objects.select_related("turma", "turma__curso")\
                          .prefetch_related("alunos", "alunos_edicao")\
                          .all()

# Filtro no banco, não em Python
eventos = Eventos.objects.filter(data_do_evento__gte=date.today())
```

---

## ⚙️ Configuração de Ambiente

### Variáveis de Ambiente Obrigatórias (`.env`)

```bash
# Django
DJANGO_SECRET_KEY="sua-chave-secreta-super-longa-e-aleatoria"
DJANGO_DEBUG="False"  # "True" apenas em desenvolvimento
ALLOWED_HOSTS="inova-edu.onrender.com,localhost,127.0.0.1"

# Database (Render fornece DATABASE_URL)
DATABASE_URL="postgresql://user:pass@host:port/db"
# OU para MySQL local:
DB_NAME="inova_edu"
DB_USER="usuario"
DB_PASSWORD="senha"
DB_HOST="127.0.0.1"
DB_PORT="3306"

# Email (Resend)
RESEND_API_KEY="re_xxxxxxxxxxxxx"
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.resend.com"
EMAIL_PORT="587"
EMAIL_USE_TLS="True"
EMAIL_HOST_USER="resend"
EMAIL_HOST_PASSWORD="re_xxxxxxxxxxxxx"

# Cloudinary
CLOUDINARY_CLOUD_NAME="seu-cloud-name"
CLOUDINARY_API_KEY="123456789012345"
CLOUDINARY_API_SECRET="abcdefghijklmnopqrstuvwxyz"
```

### Configuração de Produção (Render.com)
- `DJANGO_DEBUG=False`
- `SECURE_SSL_REDIRECT=True`
- `SECURE_HSTS_SECONDS=31536000`
- Static files servidos por WhiteNoise
- Media files no Cloudinary
- Logs em `logs/security.log`

---

## ✅ Checklist de Segurança para Mudanças Futuras

### Antes de Qualquer PR/Commit

#### Autenticação/Autorização
- [ ] Nova view protegida verifica `request.session.get("usuario_email")`?
- [ ] Verifica ownership do objeto antes de modificar/deletar?
- [ ] Usa `get_object_or_404` com filtro de permissão?
- [ ] Rate limiting aplicado em endpoints sensíveis (login, reset, upload)?

#### Validação de Entrada
- [ ] Todos inputs validados (tipo, tamanho, formato)?
- [ ] File uploads passam por `validate_file_upload()`?
- [ ] Sanitização de nomes de arquivo (`sanitize_filename`)?
- [ ] IDs validados com try/except (ValueError, TypeError)?

#### Output Encoding
- [ ] Templates usam auto-escaping do Django (padrão)?
- [ ] JSON para JS usa `|escapejs`?
- [ ] CSP nonce em scripts/estilos inline novos?

#### Segredos
- [ ] ZERO secrets hardcoded?
- [ ] Novas chaves API em variáveis de ambiente?
- [ ] `.env` no `.gitignore`?

#### Logs
- [ ] `logger.warning/error` para eventos de segurança?
- [ ] Sem `print()` em produção?
- [ ] Logs não vazam PII/senhas/tokens?

#### Headers/Config
- [ ] Novas views usam `@never_cache` se mutam estado?
- [ ] CSP atualizado se novo domínio CDN/font?
- [ ] `safe_redirect()` usado em vez de `HTTP_REFERER` direto?

#### Testes Manuais
- [ ] Login/logout funciona?
- [ ] Rate limit bloqueia após X tentativas?
- [ ] CSRF token válido em forms/AJAX?
- [ ] Upload de arquivo bloqueia extensões perigosas?
- [ ] Password reset invalida token após uso?
- [ ] Sessão expira ao fechar browser?
- [ ] HTTPS forçado em produção?

---

## 🚀 Comandos Úteis

```bash
# Desenvolvimento
cd Web
python manage.py runserver

# Migrações
python manage.py makemigrations
python manage.py migrate

# Static files (produção)
python manage.py collectstatic --noinput

# Superuser
python manage.py createsuperuser

# Shell Django
python manage.py shell

# Verificar deploy (checklist)
python manage.py check --deploy

# Testes
python manage.py test
```

---

## 📚 Referências de Segurança

- [Django Security Docs](https://docs.djangoproject.com/en/6.0/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [django-csp Documentation](https://github.com/mozilla/django-csp)
- [django-ratelimit Documentation](https://github.com/jsocol/django-ratelimit)
- [Content Security Policy Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

---

## 📌 Notas para Próximos Agentes

1. **NÃO remova** `@ratelimit`, `@never_cache`, `safe_redirect` - são proteções essenciais
2. **NÃO adicione** `@csrf_exempt` - use `{% csrf_token %}` e header `X-CSRFToken`
3. **SEMPRE** use `usuario.set_password()` e `usuario.check_password()` 
4. **SEMPRE** valide file uploads com `validate_file_upload()`
5. **MANTENHA** secrets apenas em variáveis de ambiente
6. **LOGUE** eventos de segurança com `logger.warning/error`
7. **TESTE** rate limits e CSRF após mudanças em auth/views sensíveis

---

*Documento gerado após auditoria de segurança completa - Janeiro 2025*
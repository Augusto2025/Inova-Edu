# AI Agent Guide - Inova Edu Desktop

> **Documentação técnica completa para agentes de IA que venham a manter ou estender o sistema Desktop Inova Edu.**
> 
> Versão: 2.0 | Última atualização: 2026-10-26

---

## 1. Visão Geral da Arquitetura

### 1.1 Propósito do Sistema
Aplicação desktop nativa (Windows/Linux/macOS) desenvolvida em **Python 3.11+** com **CustomTkinter** para interface gráfica, conectando-se a **PostgreSQL** via **psycopg2**. Sistema de gestão acadêmica para alunos, professores e coordenadores do Senac.

### 1.2 Stack Tecnológica
| Camada | Tecnologia | Versão | Propósito |
|--------|-----------|--------|-----------|
| GUI Framework | CustomTkinter | 5.2+ | Widgets modernos sobre tkinter |
| Database | PostgreSQL + psycopg2 | 15+ / 2.9+ | Persistência relacional |
| Config | python-dotenv | 1.0+ | Variáveis de ambiente |
| Imagens | Pillow (PIL) | 10+ | Processamento de imagens |
| Cloud Storage | Cloudinary | 1.36+ | Upload de avatares |
| Crypto | hashlib + secrets (stdlib) | — | PBKDF2-SHA256 nativo |
| Rate Limiting | Implementação própria | — | Sliding window em memória |

### 1.3 Estrutura de Diretórios
```
Desktop/
├── main.py                     # Entry point da aplicação
├── sidebar_AP.py              # Sidebar compartilhada (Aluno/Professor)
├── .env                       # SECRETS - NÃO COMMITAR (use .env.example)
├── .env.example               # Template de variáveis de ambiente
├── SECURITY_AUDIT_DESKTOP.md  # Relatório de auditoria de segurança
├── AI_AGENT_GUIDE_DESKTOP.md  # Este arquivo
├── InovaEdu.spec              # Config PyInstaller
├── assets/                    # Recursos estáticos
│   ├── cores.py               # Paleta de cores
│   ├── fonts.py               # Fontes
│   ├── header.py              # Header padrão (HeaderPadrao)
│   └── styles.py              # Estilos globais
├── config/
│   └── banco.py               # Conexão PostgreSQL (pool)
├── controllers/               # Camada de controle (MVC)
│   ├── login_controller.py    # Autenticação + rate limiting
│   ├── perfil_controller.py   # Perfil do usuário + upload Cloudinary
│   ├── projeto_controller.py  # Projetos/repositórios
│   ├── cursos_controllers.py  # Cursos
│   ├── eventos_controller.py  # Eventos
│   ├── forum_controller.py    # Fórum
│   ├── repositorio_controller.py
│   └── turma_controllers.py   # Turmas
├── models/                    # Camada de dados (MVC)
│   ├── login_model.py         # Busca usuários (retorna hash, NUNCA plain text)
│   ├── perfil_model.py        # CRUD perfil + hash de senha + validação
│   ├── sessao.py              # Singleton UsuarioSessao (SEM senha!)
│   ├── projetos_model.py
│   ├── cursos_model.py
│   ├── eventos_model.py
│   ├── forum_model.py
│   ├── repositorio_model.py
│   └── turmas_models.py
├── security/                  # Módulo de segurança (NOVO v2.0)
│   ├── __init__.py            # Exports públicos
│   ├── crypto.py              # PBKDF2-SHA256 (600k iterações)
│   ├── rate_limiter.py        # Sliding window (5 req/min, 5 min block)
│   ├── file_validator.py      # python-magic + PIL (MIME real)
│   ├── validators.py          # Senha, email, nome, bio, CPF, sanitização
│   └── logger.py              # SecureLogger + filtro de dados sensíveis
├── views/                     # Camada de visualização (MVC)
│   ├── login_view.py          # Tela de login
│   └── Aluno_e_Professor/
│       ├── home_view.py       # Dashboard principal
│       ├── profile_view.py    # Perfil (leitura)
│       ├── editar_view.py     # Edição de perfil
│       ├── projetos_view.py
│       ├── repositorio_view.py
│       ├── eventos_view.py
│       ├── forum_view.py
│       ├── turma_view.py
│       └── certificado_view.py
└── dist/                      # Build PyInstaller (ignorar no git)
```

---

## 2. Design Patterns & Convenções

### 2.1 MVC (Model-View-Controller)
- **Models** (`models/`): Acesso a dados, regras de negócio, validação, hashing
- **Views** (`views/`): Apenas UI, delegam ações aos controllers
- **Controllers** (`controllers/`): Orquestram models + views, contêm lógica de fluxo

### 2.2 Singleton Session (`models/sessao.py`)
```python
class UsuarioSessao:
    _instance = None
    email = None
    nome = None
    sobrenome = None
    descricao = None
    # ⚠️ NUNCA adicione 'senha' aqui - vulnerabilidade crítica!
```
- Thread-safe via `__new__`
- Armazena **apenas** dados não-sensíveis para exibição na UI

### 2.3 Controller Pattern
Controllers recebem `view` no construtor e expõem métodos chamados pela UI:
```python
class ProfileController:
    def __init__(self, view, session_email=None):
        self.view = view
        self.model = PerfilModel()
        self.email = session_email or UsuarioSessao().email
```

### 2.4 Assíncrono com Threading
Operações de rede (Cloudinary, download de imagens) usam `threading.Thread(daemon=True)` + `janela.after(0, callback)` para atualizar UI na thread principal.

---

## 3. Segurança - Implementação Detalhada

### 3.1 Armazenamento de Senhas - PBKDF2-SHA256
**Arquivo:** `security/crypto.py`

```python
PBKDF2_ITERATIONS = 600_000  # Igual ao Django padrão (2024+)

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    hash_value = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${hash_value.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    # Formato: pbkdf2_sha256$iterations$salt$hash
    parts = stored_hash.split('$')
    iterations = int(parts[1])
    salt = bytes.fromhex(parts[2])
    expected_hash = bytes.fromhex(parts[3])
    computed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    return constant_time_compare(computed, expected_hash)

def hash_needs_rehash(stored_hash: str) -> bool:
    """Verifica se hash precisa ser atualizado (ex: iterações antigas)."""
    try:
        parts = stored_hash.split('$')
        return int(parts[1]) < PBKDF2_ITERATIONS
    except:
        return True  # Formato desconhecido = rehash
```

**Migração de senhas legadas (texto plano):**
```sql
-- Execute no PostgreSQL para migrar usuários existentes
UPDATE usuario SET "Senha" = 'pbkdf2_sha256$600000$' || encode(gen_random_bytes(16), 'hex') || '$' || 
    encode(hashlib.pbkdf2_hmac('sha256', "Senha".encode(), gen_random_bytes(16), 600000), 'hex')
WHERE "Senha" NOT LIKE 'pbkdf2_sha256$%';
```
> ⚠️ O SQL acima é ilustrativo. Use script Python com `hash_password()` para migração real.

### 3.2 Rate Limiting - Sliding Window
**Arquivo:** `security/rate_limiter.py`

```python
class RateLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: int = 60, block_duration: int = 300):
        # max_requests: requisições permitidas
        # window_seconds: janela deslizante (1 min)
        # block_duration: tempo de bloqueio (5 min)
    
    def check_rate_limit(self, key: str) -> tuple[bool, int, int]:
        # Retorna: (allowed, remaining, retry_after_seconds)
```

**Uso no login_controller.py:**
```python
from security.rate_limiter import login_limiter

allowed, remaining, retry_after = login_limiter.check_rate_limit(user)
if not allowed:
    return (f"Muitas tentativas. Tente em {retry_after}s.", False)

# Em sucesso:
login_limiter.reset(user)  # Limpa contador
```

### 3.3 Validação de Upload de Imagens
**Arquivo:** `security/file_validator.py`

```python
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def validate_image_upload(filepath: str) -> tuple[bool, str]:
    # 1. Verifica extensão
    # 2. Verifica tamanho
    # 3. Verifica MIME REAL via python-magic (libmagic)
    # 4. Verifica assinatura do arquivo (magic bytes)
    # 5. Verifica se PIL consegue abrir (não corrompido)
```

### 3.4 Validadores de Entrada
**Arquivo:** `security/validators.py`

| Função | Regra |
|--------|-------|
| `validate_password()` | Mín 8 chars, maiúscula, minúscula, dígito, especial |
| `validate_email_address()` | RFC 5322 via email-validator |
| `validate_name()` | 2-50 chars, apenas letras/espaços/hífens/apóstrofos |
| `validate_bio()` | Máx 500 chars, sanitiza HTML |
| `sanitize_html()` | Remove tags/script/iframe (bleach) |
| `sanitize_sql_input()` | Remove ; -- /* */ xp_ etc |
| `validate_cpf()` | Algoritmo oficial brasileiro |

### 3.5 Logging Seguro
**Arquivo:** `security/logger.py`

```python
class SensitiveDataFilter(logging.Filter):
    """Remove senhas, tokens, emails, CPFs, chaves de logs."""
    PATTERNS = [
        (r'(senha|password|pwd|secret|token|api[_-]?key)["\']?\s*[:=]\s*["\']?[^"\'\s]+', r'\1=***REDACTED***'),
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),
        (r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b', '[CPF]'),
    ]

def get_logger(name: str) -> logging.Logger:
    # Configura handler com SensitiveDataFilter
    # Nível INFO para console, DEBUG para arquivo (se configurado)
```

**Uso:**
```python
from security.logger import get_logger
logger = get_logger(__name__)
logger.info(f"Login user: {email}")  # Email será mascarado nos logs
```

---

## 4. Fluxos Críticos

### 4.1 Autenticação (Login)
```
login_view.py (UI)
    → login_controller.autenticar(email, senha)
        → login_limiter.check_rate_limit(email)  # Rate limit
        → LoginUsuario.exibir_usuarios()  # Busca TODOS (pequena base)
        → verify_password(senha_plana, hash_banco)  # PBKDF2
        → login_limiter.reset(email)  # Success = limpa contador
        → UsuarioSessao().email = email  # Singleton session
    → Home view (Aluno/Professor) ou Coordenador
```

### 4.2 Atualização de Perfil com Senha
```
editar_view.py (UI)
    → abrir_modal_senha()  # Modal customizado
    → valida confirmação
    → self.nova_senha_definida = senha
    → salvar_alteracoes()
        → controller.salvar_alteracoes_perfil(nome, sobrenome, bio, senha_final, foto)
            → PerfilModel.salvar_usuario()
                → validate_password(senha)  # Política de força
                → hash_password(senha)  # PBKDF2
                → UPDATE usuario SET ... "Senha" = hash ...
            → Cloudinary upload (se nova foto)
        → UsuarioSessao().nome/sobrenome/descricao = novos valores  # SEM senha!
```

### 4.3 Upload de Avatar para Cloudinary
```
perfil_controller.salvar_alteracoes_perfil()
    → validate_image_upload(caminho_local)  # MIME + magic bytes + PIL
    → cloudinary.uploader.upload(pasta="usuario_avatares")
    → Retorna secure_url (HTTPS)
    → UPDATE usuario SET "imagem_usuario" = secure_url
```

---

## 5. Banco de Dados - Schema Relevante

### 5.1 Tabela `usuario`
```sql
CREATE TABLE usuario (
    "idUsuario" SERIAL PRIMARY KEY,
    "Nome" VARCHAR(100) NOT NULL,
    "Sobrenome" VARCHAR(100) NOT NULL,
    "Email" VARCHAR(255) UNIQUE NOT NULL,
    "Senha" TEXT NOT NULL,           -- PBKDF2 hash: pbkdf2_sha256$600000$salt$hash
    "Tipo" VARCHAR(20) NOT NULL,     -- 'Aluno', 'Professor', 'Coordenador'
    "Descricao" TEXT,
    "imagem_usuario" TEXT,           -- URL Cloudinary ou path relativo
    "data_criacao" TIMESTAMP DEFAULT NOW()
);
```

### 5.2 Conexão (`config/banco.py`)
```python
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

# Pool de conexões (thread-safe)
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1, maxconn=10,
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

def conectar():
    return connection_pool.getconn()

def liberar(conn):
    connection_pool.putconn(conn)
```

---

## 6. Variáveis de Ambiente (.env)

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `CLOUD_NAME` | Sim | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Sim | Cloudinary API Key |
| `CLOUDINARY_API_SECRET` | Sim | Cloudinary API Secret |
| `DB_HOST` | Sim | PostgreSQL host |
| `DB_PORT` | Sim | PostgreSQL port (padrão 5432) |
| `DB_NAME` | Sim | Nome do database |
| `DB_USER` | Sim | Usuário PostgreSQL |
| `DB_PASSWORD` | Sim | Senha PostgreSQL |

> ⚠️ **NUNCA** commite `.env` real. Use `.env.example` como template.

---

## 7. Build & Deploy

### 7.1 Desenvolvimento
```bash
# Instalar dependências
pip install customtkinter psycopg2-binary python-dotenv pillow cloudinary python-magic bleach email-validator

# Windows: python-magic requer libmagic.dll no PATH
# Instalar via: https://github.com/ahupp/python-magic#windows

# Executar
python main.py
```

### 7.2 Build Executável (PyInstaller)
```bash
# Via spec file (recomendado)
pyinstaller InovaEdu.spec

# Ou direto
pyinstaller --noconfirm --onefile --windowed \
  --add-data "assets;assets" \
  --add-data "config;config" \
  --add-data "controllers;controllers" \
  --add-data "models;models" \
  --add-data "security;security" \
  --add-data "views;views" \
  --add-data ".env;." \
  --hidden-import=psycopg2 \
  --hidden-import=cloudinary \
  --hidden-import=magic \
  main.py
```

**InovaEdu.spec** já configurado com:
- `--noconfirm --onefile --windowed`
- Dados: assets, config, controllers, models, security, views
- Hidden imports para psycopg2, cloudinary, magic

### 7.3 Deploy
- Executável em `dist/InovaEdu/InovaEdu.exe`
- Copie `.env` para mesma pasta do executável
- Teste em máquina limpa (sem Python)

---

## 8. Checklist de Segurança para Novas Features

Antes de commitar qualquer alteração, verifique:

- [ ] **Senhas**: Sempre use `hash_password()` / `verify_password()` - nunca armazene/plain text
- [ ] **Session**: Nunca adicione `senha` em `UsuarioSessao` (models/sessao.py)
- [ ] **Rate Limit**: Adicione `login_limiter.check_rate_limit()` em endpoints de auth
- [ ] **Upload**: Use `validate_image_upload()` ANTES de qualquer upload
- [ ] **Input**: Valide com `validate_*()` / `sanitize_*()` de `security.validators`
- [ ] **Logs**: Use `get_logger(__name__)` - nunca `print()` com dados sensíveis
- [ ] **SQL**: Sempre use queries parametrizadas (`%s`), nunca f-strings
- [ ] **Secrets**: Variáveis sensíveis só em `.env` / variáveis de ambiente
- [ ] **Crypto**: Não implemente crypto próprio - use `security.crypto`

---

## 9. Problemas Conhecidos & Soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| `ModuleNotFoundError: magic` | python-magic não instalado / libmagic faltando | Windows: baixar `magic1.dll` + colocar no PATH; Linux: `apt install libmagic1` |
| Cloudinary upload falha | Credenciais incorretas / .env não carregado | Verificar `load_dotenv()` path; checar variáveis no .env |
| Rate limit não funciona | `login_limiter` é global, mas threading pode criar instâncias | `login_limiter` é instância única em `security/__init__.py` |
| Imagem não carrega | URL Cloudinary incorreta | Verificar se `imagem_usuario` no banco tem URL completa ou path relativo |
| `psycopg2.pool.PoolError` | Pool exaurido | Aumentar `maxconn` em `config/banco.py` ou fechar conexões em `finally` |

---

## 10. Extensibilidade - Como Adicionar Features

### 10.1 Novo Controller/Model/View
1. Crie `models/novo_model.py` com validação + crypto
2. Crie `controllers/novo_controller.py` recebendo `view`
3. Crie `views/Aluno_e_Professor/novo_view.py` chamando controller
4. Registre no `sidebar_AP.py` se necessário

### 10.2 Novo Tipo de Usuário
1. Adicionar em `usuario."Tipo"` CHECK constraint
2. Atualizar `login_controller.py` roteamento pós-login
3. Criar views específicas se necessário

### 10.3 Nova Validação
Adicionar em `security/validators.py` e exportar no `security/__init__.py`

---

## 11. Referências de Arquivos-Chave

| Funcionalidade | Arquivo Principal |
|----------------|-------------------|
| Hash/Verify senha | `security/crypto.py` |
| Rate limiting login | `security/rate_limiter.py` + `controllers/login_controller.py` |
| Validação upload | `security/file_validator.py` + `controllers/perfil_controller.py` |
| Validação entrada | `security/validators.py` |
| Logging seguro | `security/logger.py` |
| Session (sem senha!) | `models/sessao.py` |
| Perfil CRUD | `models/perfil_model.py` + `controllers/perfil_controller.py` |
| Login flow | `controllers/login_controller.py` + `views/login_view.py` |
| Conexão DB | `config/banco.py` |

---

## 12. Histórico de Segurança (v2.0 - 2026-10)

| Vulnerabilidade | Status | Correção |
|----------------|--------|----------|
| Senhas em texto plano no banco | ✅ Corrigido | PBKDF2-SHA256 600k iterações |
| Senha na sessão (UsuarioSessao) | ✅ Corrigido | Removido campo `senha` do singleton |
| Sem rate limiting no login | ✅ Corrigido | Sliding window 5/min + block 5min |
| Upload sem validação MIME | ✅ Corrigido | python-magic + PIL + extensão |
| Logs com dados sensíveis | ✅ Corrigido | SecureLogger + SensitiveDataFilter |
| Inputs sem sanitização | ✅ Corrigido | validators.py (HTML, SQL, email, etc) |
| Secrets hardcoded | ✅ Corrigido | .env + .env.example template |
| Hash fraco (SHA256 simples) | ✅ Corrigido | PBKDF2 com salt aleatório |

---

## 13. Contato & Suporte

Para dúvidas sobre esta arquitetura ou relatórios de segurança:
- Consulte `SECURITY_AUDIT_DESKTOP.md` para detalhes da auditoria completa
- Siga o checklist da Seção 8 antes de qualquer PR
- Mantenha `.env` fora do versionamento **sempre**

---

*Documento gerado durante auditoria de segurança v2.0. Mantenha atualizado a cada mudança arquitetural.*
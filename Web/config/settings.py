from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
import secrets

# --- Diretórios e .env ---
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()  # força leitura do .env

import cloudinary

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# --- Segurança e Debug ---
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-' + secrets.token_urlsafe(50))

django_debug = os.environ.get('DJANGO_DEBUG')
if django_debug == "False":
    DEBUG = False
elif django_debug == "True" or django_debug is not None:
    DEBUG = True
else:
    DEBUG = True

print(f"[DJANGO DEBUG] {DEBUG}")

ALLOWED_HOSTS = ["inova-edu.onrender.com", "127.0.0.1", "localhost"]

# --- Aplicativos instalados ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'InovaEdu',
    'cloudinary',
    'cloudinary_storage',
]

# --- Middleware (SecurityMiddleware movido para o topo) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

# Regras de Política de Segurança de Conteúdo (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_FONT_SRC = ("'self'", "https://cdnjs.cloudflare.com", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "https://res.cloudinary.com")

# --- URLConf e Templates ---
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'InovaEdu.context_processors.usuario'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- Banco de dados ---
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    print("[DJANGO DATABASE] Conectado ao PostgreSQL")
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
            "PORT": os.environ.get("DB_PORT", "3306"),
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
    print("[DJANGO DATABASE] Conectado ao MySQL Local")

# --- Email ---
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# --- Validação de senha ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internacionalização ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Static files ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'InovaEdu/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# --- Default primary key ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Sessão e login ---
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/home'

# --- Storages ---
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- Media files ---
MEDIA_URL = '/media/'

# ==============================================================================
# CONFIGURAÇÕES DE SEGURANÇA E PROTEÇÃO DE CABEÇALHOS (AJUSTADAS)
# ==============================================================================

# Reconhecimento do proxy HTTPS do Render (Impede loops de redirecionamento)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Redireciona conexões HTTP para HTTPS em produção
SECURE_SSL_REDIRECT = not DEBUG

# 1. Proteção dos Cookies (Resolve: Cookie No HttpOnly / Without Secure Flag)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# 2. Prevenção de MIME-Sniffing (Resolve: X-Content-Type-Options Header Missing)
SECURE_CONTENT_TYPE_NOSNIFF = True

# 3. Força HTTPS no Navegador (Resolve: Strict-Transport-Security Header Not Set)
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 Ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
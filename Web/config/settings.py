from pathlib import Path
import os
from dotenv import load_dotenv
import secrets

# --- Diretórios e .env ---
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')  # força leitura do .env

# --- Configurações AWS / Tebi ---
os.environ['AWS_ACCESS_KEY_ID'] = os.getenv("TEBI_ACCESS_KEY")
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv("TEBI_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("TEBI_BUCKET_NAME")
os.environ['AWS_STORAGE_BUCKET_NAME'] = AWS_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL = "https://s3.tebi.io"
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_USE_SSL = True
AWS_S3_SIGNATURE_VERSION = 's3'

# --- Segurança ---
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-' + secrets.token_urlsafe(50))
DEBUG = True
ALLOWED_HOSTS = []

# --- Aplicativos instalados ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'InovaEdu',
    'storages',  # para S3
]

# --- Armazenamento de arquivos ---
try:
    from InovaEdu.storage import TebiStorage
    test_storage = TebiStorage()
    DEFAULT_FILE_STORAGE = "InovaEdu.storage.TebiStorage"
    from django.core.files.storage import default_storage
    default_storage._wrapped = test_storage
except Exception as e:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.tebi.io'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
MEDIA_ROOT = ''

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        'HOST': os.environ.get('HOST'),
        'PORT': os.environ.get('PORT'),
        'PASSWORD': os.environ.get('PASSWORD'),
    }
}

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
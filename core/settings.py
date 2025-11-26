from pathlib import Path
import os
import environ

# 1. Definição do diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Leitura do .env (Forçando o caminho para funcionar no Windows)
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 3. Configurações de Segurança
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# 4. Aplicações Instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # Obrigatório para o Allauth
    
    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Libs de Terceiros
    'storages', # AWS S3
    'widget_tweaks',
    
    # Meus Apps
    'accounts',
    'companies',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Estáticos em Produção
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # Middleware do Allauth
    'core.middleware.LoginRequiredMiddleware',
    'companies.middleware.CompanyMiddleware', 
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request', # Necessário para o Allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# 5. Banco de Dados (Conecta no Postgres via URL do .env)
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# 6. Modelo de Usuário Customizado (Sem username, com nome e telefone)
AUTH_USER_MODEL = 'accounts.CustomUser'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# 7. Internacionalização (Brasil)
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# 8. Arquivos Estáticos e Media (Configuração Híbrida Local/S3)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Se houver chaves AWS no .env, usa S3 para upload de usuarios (Media)
if env('AWS_ACCESS_KEY_ID', default=None):
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    # Desenvolvimento Local
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 9. Configurações do Allauth (MODERNIZADO E SEM WARNINGS)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Define login apenas por email
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_USER_MODEL_USERNAME_FIELD = None 

ACCOUNT_SIGNUP_FIELDS = [
    'email*',        # O asterisco torna obrigatório
    'password1*',    # Senha principal
    'password2*',    # Confirmação de senha (repetir senha)
]
# Aponta para nosso formulário com Nome e Telefone
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
}

# Verificação de email
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Meu Projeto] '


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = env. int('EMAIL_PORT', default=587)
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@seusite.com')



# Redirecionamentos
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = 'account_login' # Nome da rota de login do Allauth



# Adicionar no settings. py:

# ═══════════════════════════════════════════════════════════════
# ALLAUTH - SEGURANÇA
# ═══════════════════════════════════════════════════════════════

# Tempo de expiração do código de verificação (padrão: 3 dias = muito!)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # 👈 Reduzir para 1 dia

# Cooldown para reenvio de código (evita spam)
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180  # 3 minutos entre reenvios

# Máximo de tentativas de login (proteção contra brute-force)
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # 5 minutos de bloqueio

# Logout ao trocar senha (segurança)
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

# Impedir enumeração de usuários
ACCOUNT_PREVENT_ENUMERATION = True  # 👈 IMPORTANTE!

# Adicione ao settings.py
# ✅ Melhor abordagem
if env('REDIS_URL', default=None):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': env('REDIS_URL'),
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }


import sentry_sdk

if not DEBUG:
    sentry_sdk. init(
        dsn=env('SENTRY_DSN', default=''),
        send_default_pii=True,
        traces_sample_rate=0.1,  # 10% das transações
    )
    
    # Headers de segurança
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
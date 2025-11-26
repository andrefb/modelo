from pathlib import Path
import os
import environ
import sentry_sdk

# ==============================================================================
# 1. SETUP DO AMBIENTE
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])


# ==============================================================================
# 2. APLICAÇÃO E MIDDLEWARE
# ==============================================================================
INSTALLED_APPS = [
    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    
    # Third-party
    'allauth',
    'allauth.account',
    'storages',
    'widget_tweaks',
    
    # Local Apps
    'accounts',
    'companies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'core.middleware.LoginRequiredMiddleware', 
    'companies.middleware.CompanyMiddleware',
]

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==============================================================================
# 3. BANCO DE DADOS
# ==============================================================================
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# Performance: Connection Pooling Simulado
if not DEBUG:
    DATABASES['default']['CONN_MAX_AGE'] = 600


# ==============================================================================
# 4. CACHE E SESSÕES (REDIS)
# ==============================================================================
if env('REDIS_URL', default=None):
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
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


# ==============================================================================
# 5. AUTENTICAÇÃO E USUÁRIOS
# ==============================================================================
AUTH_USER_MODEL = 'accounts.CustomUser'
SITE_ID = 1

# Login & Signup
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_USER_MODEL_USERNAME_FIELD = None 
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Meu Projeto] '
ACCOUNT_PREVENT_ENUMERATION = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomSignupForm'}

# Security Logic
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_RATE_LIMITS = {
    "confirm_email": "180/3m",
    "login_failed": "5/5m",
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Redirecionamentos
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'


# ==============================================================================
# 6. INTERNACIONALIZAÇÃO
# ==============================================================================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# 7. ARQUIVOS ESTÁTICOS E MÍDIA
# ==============================================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if env('AWS_ACCESS_KEY_ID', default=None):
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    
    STORAGES = {
        "default": { "BACKEND": "storages.backends.s3.S3Storage" },
        "staticfiles": { "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage" },
    }
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'


# ==============================================================================
# 8. EMAIL
# ==============================================================================
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = env.int('EMAIL_PORT', default=587)
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@seusite.com')


# ==============================================================================
# 9. MONITORAMENTO E SEGURANÇA (PRODUÇÃO)
# ==============================================================================
if not DEBUG:
    # Sentry (Logs de Erro)
    sentry_sdk.init(
        dsn=env('SENTRY_DSN', default=''),
        send_default_pii=True,
        traces_sample_rate=0.1,
    )
    
    # Headers de Segurança HTTP
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000 # 1 ano
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
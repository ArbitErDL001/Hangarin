import os
import socket
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = 'django-insecure-aki@&eowcq#x8yk&p5o0+qu0-b5_di=9l%^1!s1@#@6s(ns!(='

DEBUG = True



ALLOWED_HOSTS = ['arbiterdl001.pythonanywhere.com', '127.0.0.1', 'localhost']

# --- Site ID logic (no model imports here) ---
# Use an environment variable when available, otherwise pick sensible defaults.
if "pythonanywhere" in socket.gethostname():
    SITE_ID = int(os.environ.get("SITE_ID", "4"))
else:
    SITE_ID = int(os.environ.get("SITE_ID", "1"))

# IMPORTANT: Do NOT import or access Django models (e.g. django.contrib.sites.models.Site)
# at module import time in settings.py — doing so raises "Apps aren't loaded yet."
# Create or update the Site row AFTER migrations have run. Example (run in shell):
#
#   python manage.py migrate
#   python manage.py shell
#   from django.conf import settings
#   from django.contrib.sites.models import Site
#   Site.objects.update_or_create(
#       pk=settings.SITE_ID,
#       defaults={'domain': os.environ.get('SITE_DOMAIN', 'localhost:8000'),
#                 'name': os.environ.get('SITE_NAME', 'Hangarin')}
#   )
#
# Alternatively, automate this in your app's AppConfig.ready() so it runs after apps are loaded.

# --- Installed apps ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hangarin.apps.HangarinConfig',
    'widget_tweaks',
    'pwa',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

ROOT_URLCONF = 'config.urls'

# --- Authentication ---
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_LOGOUT_ON_GET = True

# Remove deprecated/legacy allauth names if present.
for _name in ('ACCOUNT_LOGIN_METHOD', 'ACCOUNT_AUTHENTICATION_METHOD'):
    if _name in globals():
        del globals()[_name]

# New canonical setting for recent django-allauth versions.
# Use a set of allowed login identifiers.
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
# Note: removed ACCOUNT_SIGNUP_FIELDS to avoid account.W001 conflict.
# If you need custom signup fields, implement a custom signup form (preferred) or
# reintroduce ACCOUNT_SIGNUP_FIELDS only after ensuring it matches login configuration.

# --- Social account providers ---
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}


# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- WSGI ---
WSGI_APPLICATION = 'config.wsgi.application'

# --- Database ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# --- Static files ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Only add STATICFILES_DIRS if the directory actually exists to avoid the W004 warning.
_static_dir = BASE_DIR / 'static'
if _static_dir.exists() and _static_dir.is_dir():
    STATICFILES_DIRS = [_static_dir]
else:
    STATICFILES_DIRS = []

# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Progressive Web App ---
PWA_APP_NAME = 'Hangarin'
PWA_APP_DESCRIPTION = "A Progressive Web App version of Hangarin"
PWA_APP_THEME_COLOR = '#0A0A0A'
PWA_APP_BACKGROUND_COLOR = '#FFFFFF'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {'src': '/static/img/menu.png', 'sizes': '192x192'},
    {'src': '/static/img/profile.jpg', 'sizes': '512x512'}
]
PWA_APP_ICONS_APPLE = [
    {'src': '/static/img/menu.png', 'sizes': '192x192'},
    {'src': '/static/img/profile.jpg', 'sizes': '512x512'}
]
PWA_APP_DIR = 'ltr'
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'hangarin', 'static/js', 'serviceworker.js')

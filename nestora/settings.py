from pathlib import Path
import os

import dj_database_url


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECURITY
# =========================================================

# Default to local development so `python manage.py runserver` works without
# environment setup. Set DEBUG=False explicitly in production (for example, Appliku).
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'django-insecure-local-development-only-key'
    else:
        raise RuntimeError('Set the SECRET_KEY environment variable before starting Django.')

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ALLOWED_HOSTS += [host.strip() for host in os.environ.get('ALLOWED_HOSTS', '').split(',') if host.strip()]


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [

    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Nestora App
    'store',
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================================================
# ROOT URL
# =========================================================

ROOT_URLCONF = 'nestora.urls'


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [

    {
        'BACKEND':
            'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

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


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = 'nestora.wsgi.application'


# =========================================================
# DATABASE
# =========================================================

DATABASES = {'default': dj_database_url.config(
    default=f'sqlite:///{(BASE_DIR / "db.sqlite3").as_posix()}',
    conn_max_age=600,
    conn_health_checks=True,
)}


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================================================
# LANGUAGE & TIME
# =========================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = '/static/'


STATICFILES_DIRS = [

    BASE_DIR / 'static',

]


# =========================================================
# STATIC FILES FOR PRODUCTION
# =========================================================

STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
WHITENOISE_AUTOREFRESH = DEBUG


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# =========================================================
# LOGIN / LOGOUT
# =========================================================

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'


# =========================================================
# SESSION
# =========================================================

SESSION_COOKIE_AGE = 1209600

SESSION_SAVE_EVERY_REQUEST = False


# =========================================================
# MESSAGE TAGS
# =========================================================

from django.contrib.messages import constants as messages


MESSAGE_TAGS = {

    messages.DEBUG: 'secondary',

    messages.INFO: 'info',

    messages.SUCCESS: 'success',

    messages.WARNING: 'warning',

    messages.ERROR: 'danger',

}


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

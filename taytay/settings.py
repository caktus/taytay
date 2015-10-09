"""
Django settings for taytay project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = (
    'taytay',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'taytay.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'taytay.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='postgres:///taytay'),
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

PUBLIC_ROOT = os.environ.get('PUBLIC_ROOT', os.path.join(BASE_DIR, 'public'))

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Security settings

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ.get('DEBUG', 'on') == 'on'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(';')

INTERNAL_IPS = ('127.0.0.1', )

X_FRAME_OPTIONS = 'DENY'

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SSL_ENABLED = os.environ.get('SSL', 'off') == 'on'

SECURE_SSL_REDIRECT = SSL_ENABLED

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365 if SSL_ENABLED else 0

SESSION_COOKIE_SECURE = SSL_ENABLED

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = SSL_ENABLED

CSRF_COOKIE_HTTPONLY = True

# Logging settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s: %(levelname)s/%(name)s] - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', ]
    },
    'loggers': {
        'django': {
            'propagate': True,
        },
    }
}

# Systems checks

SILENCED_SYSTEM_CHECKS = [
    # Not enabling HSTS for all subdomains
    'security.W005'
]

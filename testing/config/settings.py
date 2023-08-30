import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

import dj_database_url

BASE_PATH = Path(__file__).parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = (os.getenv('DEBUG', 'False').upper() == 'TRUE')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost 127.0.0.1 ::1').split()

INTERNAL_IPS = ['127.0.0.1']

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_datacite'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE')),
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
  ('en', _('English')),
]

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True

BASE_URL = os.getenv('BASE_URL', '').rstrip('/') + '/'

STATIC_URL = BASE_URL + 'static/'
STATIC_ROOT = BASE_PATH / 'static_root'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

CSRF_COOKIE_PATH = BASE_URL
LANGUAGE_COOKIE_PATH = BASE_URL
SESSION_COOKIE_PATH = BASE_URL

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]

DOI_PREFIX = '10.12345'

FIXTURE_DIRS = (
    BASE_PATH / 'fixtures',
)

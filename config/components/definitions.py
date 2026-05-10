from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = ['movies/locale']

INTERNAL_IPS = ["127.0.0.1",]
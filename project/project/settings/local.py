from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env.str('DB_LOCAL_NAME'),
        'USER': env.str('DB_LOCAL_USER'),
        'PASSWORD': env.str('DB_LOCAL_PASS'),
        'HOST': env.str('DB_LOCAL_HOST'),
        'PORT': env.str('DB_LOCAL_PORT'),
    }
}

# Archivos estáticos y de medios locales
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

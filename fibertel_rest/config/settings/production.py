from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['your_server_ip_address']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER':'root',
        'PASSWORD':'tecsup2023',
        'NAME': 'fibertel_rest_db',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
}}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'


from pathlib import Path
from datetime import timedelta
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Add the apps directory to the Python path

sys.path.insert(0, str(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$%#a*zrk57l))hd@m$xh&0+kn%pp*f9r^vggr)ega*a%cri^&j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1","192.168.1.5"]
  


# Application definition

# Aplicaciones bases(por defecto)
BASE_APPS = [
    'admin_interface',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'colorfield',
]
# Aplicaciones locales(generadas por nosotros)
LOCAL_APPS = [
    'apps.accounts',
    'apps.billing',
    'apps.services',
    'apps.support',
    'apps.monitoring',
    # 'apps.notifications',
]

# Aplicaciones de terceros (Librerias externas)
THIRDS_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'rest_framework_nested',

]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),# El token expira en 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1), # Puedes renovar tokens por 1 día
    'ROTATE_REFRESH_TOKENS': True, # Cada vez que renuevas, obtienes un nuevo refresh token
    'BLACKLIST_AFTER_ROTATION': True, # El refresh token viejo se invalida
    'UPDATE_LAST_LOGIN': True,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}
# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://192.168.1.5:8000"
]
# Configuraciones adicionales de CORS
CORS_ALLOW_ALL_ORIGINS = True  # Para desarrollo
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
INSTALLED_APPS = list(BASE_APPS + LOCAL_APPS + THIRDS_APPS)

X_FRAME_OPTIONS = 'SAMEORIGIN'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',# Verifica la seguridad básica
    'corsheaders.middleware.CorsMiddleware', # Verifica si el origen está permitido
    'django.contrib.sessions.middleware.SessionMiddleware',# Maneja sesiones
    'django.middleware.common.CommonMiddleware',# Procesamiento común
    'django.middleware.csrf.CsrfViewMiddleware',# Protección contra CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Verifica la autenticación
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fibertel_rest.config.urls'


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

WSGI_APPLICATION = 'fibertel_rest.config.wsgi.application'




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTH_USER_MODEL = 'accounts.User'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os
import posixpath
import environ
import dj_database_url

# Variables de entorno
env = environ.Env()

# Construir rutas dentro del proyecto utilizando: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuración rápida de desarrollo: no apto para producción
# Ver https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: ¡mantén en secreto la clave secreta utilizada en producción!
SECRET_KEY = 'o!ld8nrt4vc*h1zoey*wj48x*q0#ss12h=+zh)kk^6b3aygg=!'

# ADVERTENCIA DE SEGURIDAD: no ejecutes con depuración activada en producción.
DEBUG = True

# Cambiar el modelo de usuario predeterminado por nuestro modelo personalizado
AUTH_USER_MODEL = 'accounts.User'

# Definición de aplicaciones

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
]

# Aplicaciones de terceros
THIRD_PARTY_APPS = [
    'crispy_forms',
    'rest_framework',
    'channels',
]

# Aplicaciones personalizadas
PROJECT_APPS = [
    'app.apps.AppConfig',
    'accounts.apps.AccountsConfig',
    'course.apps.CourseConfig',
    'result.apps.ResultConfig',
    'search.apps.SearchConfig',
]

# Combinar todas las aplicaciones
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'SMS.wsgi.application'

ASGI_APPLICATION = "SMS.asgi.application"

# Configuración de la base de datos
DATABASES = {
    'default': dj_database_url.config(default='postgres://tutorias_user:9JCvSl2wQU1MWhu5cRQVUhJuF5NbooHq@dpg-ciq927l9aq0dcprd0rhg-a.oregon-postgres.render.com/tutorias')
}

# Resto del código...
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

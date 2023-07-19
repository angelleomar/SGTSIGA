import os
from django.core.wsgi import get_wsgi_application

# Configuración de la base de datos para Render
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SMS.settings')

application = get_wsgi_application()

import os
import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter

# Establecer la variable de entorno para la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SMS.settings')

# Configurar Django
django.setup()

# Configuración de enrutamiento de protocolo para Channels
application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    # Solo se maneja el protocolo HTTP por ahora. (Podemos agregar otros protocolos más adelante).
})

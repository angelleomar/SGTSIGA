
"""Utilidad de línea de comandos de Django para tareas administrativas."""
import os
import sys
import environ

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SMS.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado y "
            "disponible en tu variable de entorno PYTHONPATH? ¿Olvidaste "
            "activar un entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Las variables de entorno del sistema operativo tienen prioridad sobre las variables de .env
    environ.Env.read_env()
    main()

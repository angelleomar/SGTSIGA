from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=Http404):
    """
  Decorator para vistas que comprueba que el usuario que ha iniciado sesión es un estudiante,
     redirige a la página de inicio de sesión si es necesario.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def lecturer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=Http404):
    """
  Decorador para vistas que comprueba que el usuario que ha iniciado sesión es un profesor,
     redirige a la página de inicio de sesión si es necesario.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_lecturer or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=Http404):
    """
  Decorador para vistas que comprueba que el usuario que ha iniciado sesión es un profesor,
     redirige a la página de inicio de sesión si es necesario.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

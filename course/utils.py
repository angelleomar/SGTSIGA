import datetime 
import os
import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    """
    Genera una cadena aleatoria de longitud 'size' utilizando los caracteres especificados.
    El valor predeterminado para 'size' es 10.
    Puedes proporcionar un tamaño diferente si lo deseas.
    """
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    Genera un slug único basado en el título de una instancia de modelo.
    Si se proporciona un 'new_slug' opcionalmente, se utilizará en lugar de slugificar el título.
    La función slugifica el título utilizando la función 'slugify' de Django,
    que reemplaza espacios y caracteres especiales por guiones.
    Luego, verifica si ese slug ya existe en la base de datos.
    Si el slug existe, agrega una cadena aleatoria generada por 'random_string_generator' al final del slug
    y vuelve a verificar la unicidad.
    Este proceso se repite hasta que se genera un slug único.
    El slug único se devuelve como resultado.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.Titulo)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

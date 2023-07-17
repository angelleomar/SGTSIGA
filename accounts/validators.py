import re
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    """
    Validador de nombres de usuario ASCII.
    Valida que un nombre de usuario solo contenga letras en inglés, números y los caracteres @/./+/-/_.
    """
    regex = r'^[a-zA-Z]+\/(...)\/(....)'  # Patrón de expresión regular para validar el nombre de usuario
    message = _(
        'Introduzca un nombre de usuario válido. Este valor puede contener solo letras en inglés,'
        'números y @/./+/-/_ caracteres.'
    )
    flags = re.ASCII


from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Student, Parent

class UserAdmin(admin.ModelAdmin):
    """
    Clase de configuración para el modelo User en el administrador de Django.
    Personaliza la apariencia y el comportamiento del modelo en el administrador.
    """
    list_display = ['get_full_name', 'username', 'email', 'is_active', 'is_student', 'is_lecturer', 'is_parent', 'is_staff']
    """
    Campo utilizado para especificar qué campos se mostrarán en la lista de visualización
    del modelo en el administrador. Los campos se muestran en el mismo orden que se 
    definen en la lista.
    """
    search_fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_lecturer', 'is_parent', 'is_staff']
    """
    Campo utilizado para especificar los campos que se utilizarán para la búsqueda de
    registros en el modelo en el administrador. Los registros se pueden buscar por los
    campos especificados en la lista.
    """

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        """
        Clase Meta utilizada para proporcionar metadatos adicionales sobre la configuración
        del modelo. Aquí se especifica el nombre singular y plural del modelo que se mostrará
        en el administrador.

        - managed: Indica si el modelo es administrado por Django.
        - verbose_name: Nombre singular del modelo que se muestra en el administrador.
        - verbose_name_plural: Nombre plural del modelo que se muestra en el administrador.
        """

admin.site.register(User, UserAdmin)
"""
Registra el modelo User en el administrador de Django utilizando la configuración definida
en la clase UserAdmin.
"""
admin.site.register(Student)
"""
Registra el modelo Student en el administrador de Django sin configuración adicional.
Se utilizarán las configuraciones predeterminadas del administrador.
"""
admin.site.register(Parent)
"""
Registra el modelo Parent en el administrador de Django sin configuración adicional.
Se utilizarán las configuraciones predeterminadas del administrador.
"""

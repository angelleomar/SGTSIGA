from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Session, Semester, NewsAndEvents

# Registra el modelo Semester en el panel de administración
admin.site.register(Semester)

# Registra el modelo Session en el panel de administración
admin.site.register(Session)

# Registra el modelo NewsAndEvents en el panel de administración
admin.site.register(NewsAndEvents)

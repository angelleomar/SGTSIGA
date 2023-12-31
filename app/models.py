from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

# Definición de opciones para el campo "Tipo" del modelo NewsAndEvents
NEWS = "News"
EVENTS = "Event"

POST = (
    (NEWS, "Noticia"),
    (EVENTS, "Evento"),
)

# Definición de opciones para el campo "semester" del modelo Semester
FIRST = "Primero"
SECOND = "Segundo"
THIRD = "Tercero"

SEMESTER = (
    (FIRST, "Primero"),
    (SECOND, "Segundo"),
    (THIRD, "Tercero"),
)


class NewsAndEventsQuerySet(models.query.QuerySet):
    """
    Clase QuerySet personalizada para el modelo NewsAndEvents.
    Proporciona métodos adicionales para buscar registros basados en un criterio de búsqueda.
    """

    def search(self, query):
        lookups = (Q(Titulo__icontains=query) |
                   Q(Descripcion__icontains=query) |
                   Q(Tipo__icontains=query)
                   )
        return self.filter(lookups).distinct()


class NewsAndEventsManager(models.Manager):
    """
    Clase Manager personalizada para el modelo NewsAndEvents.
    Permite realizar consultas y búsquedas personalizadas en el modelo.
    """

    def get_queryset(self):
        return NewsAndEventsQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)  # NewsAndEvents.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().search(query)


class NewsAndEvents(models.Model):
    """
    Modelo para representar noticias y eventos.
    """

    Titulo = models.CharField(max_length=200, null=True)
    Descripcion = models.TextField(max_length=200, blank=True, null=True)
    Tipo = models.CharField(choices=POST, max_length=10)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    objects = NewsAndEventsManager()

    def __str__(self):
        return self.Titulo


class Session(models.Model):
    """
    Modelo para representar una sesión.
    """

    session = models.CharField(max_length=200, unique=True)
    is_current_session = models.BooleanField(default=False, blank=True, null=True)
    next_session_begins = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.session


class Semester(models.Model):
    """
    Modelo para representar un semestre.
    """

    semester = models.CharField(max_length=10, choices=SEMESTER, blank=True)
    is_current_semester = models.BooleanField(default=False, blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    next_semester_begins = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.semester

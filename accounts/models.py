from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings

from django.db.models import Q
from PIL import Image

from course.models import Program
from .validators import ASCIIUsernameValidator


# Constantes de nivel académico
BACHLOAR_DEGREE = "Licenciatura"
MASTER_DEGREE = "Maestría"

LEVEL = (
    (BACHLOAR_DEGREE, "Licenciatura"),
    (MASTER_DEGREE, "Maestría"),
)

# Constantes para la relación entre padres e hijos
FATHER = "Padre"
MOTHER = "Madre"
BROTHER = "Hermano"
SISTER = "Hermana"
GRAND_MOTHER = "Abuela"
GRAND_FATHER = "Abuelo"
OTHER = "Otro"

RELATION_SHIP  = (
    (FATHER, "Padre"),
    (MOTHER, "Madre"),
    (BROTHER, "Hermano"),
    (SISTER, "Hermana"),
    (GRAND_MOTHER, "Abuela"),
    (GRAND_FATHER, "Abuelo"),
    (OTHER, "Otro"),
)

# Manager personalizado para el modelo User
class UserManager(UserManager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(username__icontains=query) | 
                         Q(first_name__icontains=query)| 
                         Q(last_name__icontains=query)| 
                         Q(email__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct()
        return qs


# Modelo personalizado para el usuario
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_dep_head = models.BooleanField(default=False)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pictures/%Y/%m/%d/', default='default.png', null=True)
    email = models.EmailField(blank=True, null=True)

    username_validator = ASCIIUsernameValidator()

    objects = UserManager()

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return '{} ({})'.format(self.username, self.get_full_name)

    @property
    def get_user_role(self):
        if self.is_superuser:
            return "Administrador"
        elif self.is_student:
            return "Estudiante"
        elif self.is_lecturer:
            return "Profesor"
        elif self.is_parent:
            return "Padre"

    def get_picture(self):
        try:
            return self.picture.url
        except:
            no_picture = settings.MEDIA_URL + 'default.png'
            return no_picture

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.picture.url != settings.MEDIA_URL + 'default.png':
            self.picture.delete()
        super().delete(*args, **kwargs)


# Manager personalizado para el modelo Student
class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(level__icontains=query) | 
                         Q(department__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct()
        return qs


# Modelo para representar a un estudiante
class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    department = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)

    objects = StudentManager()

    def __str__(self):
        return self.student.get_full_name

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def delete(self, *args, **kwargs):
        self.student.delete()
        super().delete(*args, **kwargs)


# Modelo para representar a un padre
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    relation_ship = models.TextField(choices=RELATION_SHIP, blank=True)

    def __str__(self):
        return self.user.username


# Modelo para representar a un jefe de departamento
class DepartmentHead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{}".format(self.user)

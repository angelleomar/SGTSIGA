from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm

from course.models import Program
from .models import User, Student, LEVEL, RELATION_SHIP

# Formulario para agregar personal (lectores)
class StaffAddForm(UserCreationForm):
    # Definición de los campos del formulario y sus atributos
    username = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Nombre de usuario"
    )
    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Nombre(s)"
    )
    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Apellidos"
    )
    address = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Dirección"
    )
    phone = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Número de teléfono"
    )
    email = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Correo electrónico"
    )
    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}),
        label="Contraseña"
    )
    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}),
        label="Confirmar contraseña"
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


# Formulario para agregar estudiantes
class StudentAddForm(UserCreationForm):
    # Definición de los campos del formulario y sus atributos
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'username_id'}),
        label="Nombre de usuario"
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Dirección"
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Número de teléfono"
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Nombre(s)"
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Apellidos"
    )
    level = forms.CharField(
        widget=forms.Select(
            choices=LEVEL,
            attrs={'class': 'browser-default custom-select form-control'}
        )
    )
    department = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select form-control'}),
        label="Departamento"
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}),
        label="Correo electrónico"
    )
    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}),
        label="Contraseña"
    )
    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}),
        label="Confirmar contraseña"
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.phone = self.cleaned_data.get('phone')
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(
            student=user,
            level=self.cleaned_data.get('level'),
            department=self.cleaned_data.get('department')
        )
        student.save()
        return user


# Formulario para actualizar el perfil de un usuario
class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}),
        label="Correo electrónico"
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Nombre(s)"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Apellidos"
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Número de teléfono"
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Dirección / Ciudad"
    )

    class Meta:
        model = User
        fields = ['email', 'phone', 'address', 'picture', 'first_name', 'last_name']


# Formulario para validación de correo electrónico en el restablecimiento de contraseña
class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "No hay ningún usuario registrado con la dirección de correo electrónico especificada."
            self.add_error('email', msg)
            return email


# Formulario para agregar padres
class ParentAddForm(UserCreationForm):
    # Definición de los campos del formulario y sus atributos
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Nombre de usuario"
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Dirección"
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Número de teléfono"
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Nombres"
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label="Apellidos"
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}),
        label="Correo electrónico"
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select form-control'}),
        label="Estudiante"
    )
    relation_ship = forms.CharField(
        widget=forms.Select(
            choices=RELATION_SHIP,
            attrs={'class': 'browser-default custom-select form-control'}
        ),
    )
    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}),
        label="Contraseña"
    )
    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}),
        label="Confirmar contraseña"
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_parent = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.phone = self.cleaned_data.get('phone')
        user.email = self.cleaned_data.get('email')
        user.save()
        parent = Parent.objects.create(
            user=user,
            student=self.cleaned_data.get('student'),
            relation_ship=self.cleaned_data.get('relation_ship')
        )
        parent.save()
        return user
    """
    En resumen, estos formularios se utilizan para interactuar con los modelos de Django y proporcionar una 
    interfaz para crear y actualizar usuarios, estudiantes, padres, etc. Cada formulario define 
    los campos necesarios y sus 
    atributos, y los métodos save() se utilizan para guardar los datos ingresados en los modelos correspondientes.
    """
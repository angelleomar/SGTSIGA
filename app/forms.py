from django import forms
from django.db import transaction

from .models import NewsAndEvents, Session, Semester, SEMESTER


class NewsAndEventsForm(forms.ModelForm):
    """
    Formulario para el modelo NewsAndEvents.
    Permite crear y editar noticias y eventos.
    """

    class Meta:
        model = NewsAndEvents
        fields = ('Titulo', 'Descripcion', 'Tipo',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Titulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['Descripcion'].widget.attrs.update({'class': 'form-control'})
        self.fields['Tipo'].widget.attrs.update({'class': 'form-control'})


class SessionForm(forms.ModelForm):
    """
    Formulario para el modelo Session.
    Permite crear y editar sesiones.
    """

    next_session_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
            }
        ),
        required=True)

    class Meta:
        model = Session
        fields = ['session', 'is_current_session', 'next_session_begins']


class SemesterForm(forms.ModelForm):
    """
    Formulario para el modelo Semester.
    Permite crear y editar semestres.
    """

    semester = forms.CharField(
        widget=forms.Select(
            choices=SEMESTER,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="Semestre",
    )
    is_current_semester = forms.CharField(
        widget=forms.Select(
            choices=((True, 'Sí'), (False, 'No')),
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="¿Es el semestre actual?",
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        required=True
    )

    next_semester_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        ),
        required=True)

    class Meta:
        model = Semester
        fields = ['semester', 'is_current_semester', 'session', 'next_semester_begins']

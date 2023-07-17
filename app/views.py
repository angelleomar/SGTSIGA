from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from accounts.decorators import admin_required, lecturer_required
from .forms import SessionForm, SemesterForm, NewsAndEventsForm
from .models import *


# ########################################################
# NOTICIAS & EVENTOS
# ########################################################

@login_required
def home_view(request):
    """
    Vista para mostrar la página de inicio con las noticias y eventos más recientes.
    """
    items = NewsAndEvents.objects.all().order_by('-updated_date')
    context = {
        'Titulo': "Noticias y Eventos | SGT",
        'items': items,
    }
    return render(request, 'app/index.html', context)


@login_required
def post_add(request):
    """
    Vista para agregar una nueva publicación de noticias o eventos.
    """
    if request.method == 'POST':
        form = NewsAndEventsForm(request.POST)
        Titulo = request.POST.get('Titulo')
        if form.is_valid():
            form.save()
            messages.success(request, (Titulo + ' ha sido subido.'))
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrija los siguientes errores.')
    else:
        form = NewsAndEventsForm()
    return render(request, 'app/post_add.html', {
        'Titulo': 'Añadir publicación | SGT',
        'form': form,
    })


@login_required
@lecturer_required
def edit_post(request, pk):
    """
    Vista para editar una publicación existente de noticias o eventos.
    """
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    if request.method == 'POST':
        form = NewsAndEventsForm(request.POST, instance=instance)
        Titulo = request.POST.get('Titulo')
        if form.is_valid():
            form.save()
            messages.success(request, (Titulo + 'Ha sido actualizado.'))
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrija los siguientes errores.')
    else:
        form = NewsAndEventsForm(instance=instance)
    return render(request, 'app/post_add.html', {
        'Titulo': 'Editar post | SGT',
        'form': form,
    })


@login_required
@lecturer_required
def delete_post(request, pk):
    """
    Vista para eliminar una publicación existente de noticias o eventos.
    """
    post = get_object_or_404(NewsAndEvents, pk=pk)
    Titulo = post.Titulo
    post.delete()
    messages.success(request, (Titulo + 'ha sido eliminado.'))
    return redirect('home')


# ########################################################
# Sesion
# ########################################################

@login_required
@lecturer_required
def session_list_view(request):
    """
    Vista para mostrar la lista de todas las sesiones.
    """
    sessions = Session.objects.all().order_by('-is_current_session', '-session')
    return render(request, 'app/session_list.html', {"sessions": sessions})


@login_required
@lecturer_required
def session_add_view(request):
    """
    Vista para agregar una nueva sesión.
    """
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            data = form.data.get('is_current_session')  # devuelve una cadena 'True' si el usuario seleccionó Sí
            if data == 'true':
                sessions = Session.objects.all()
                if sessions:
                    for session in sessions:
                        if session.is_current_session == True:
                            unset = Session.objects.get(is_current_session=True)
                            unset.is_current_session = False
                            unset.save()
                    form.save()
                else:
                    form.save()
            else:
                form.save()
            messages.success(request, 'Sesión añadida con éxito.')
            return redirect('session_list')
    else:
        form = SessionForm()
    return render(request, 'app/session_update.html', {'form': form})


@login_required
@lecturer_required
def session_update_view(request, pk):
    """
    Vista para actualizar una sesión existente.
    """
    session = Session.objects.get(pk=pk)
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        data = form.data.get('is_current_session')
        if data == 'true':
            sessions = Session.objects.all()
            if sessions:
                for session in sessions:
                    if session.is_current_session == True:
                        unset = Session.objects.get(is_current_session=True)
                        unset.is_current_session = False
                        unset.save()
            if form.is_valid():
                form.save()
                messages.success(request, 'Sesión actualizada con éxito.')
                return redirect('session_list')
        else:
            form = SessionForm(request.POST, instance=session)
            if form.is_valid():
                form.save()
                messages.success(request, 'Sesión actualizada con éxito.')
                return redirect('session_list')
    else:
        form = SessionForm(instance=session)
    return render(request, 'app/session_update.html', {'form': form})


@login_required
@lecturer_required
def session_delete_view(request, pk):
    """
    Vista para eliminar una sesión existente.
    """
    session = get_object_or_404(Session, pk=pk)
    if session.is_current_session:
        messages.error(request, "No puede eliminar la sesión actual")
        return redirect('session_list')
    else:
        session.delete()
        messages.success(request, "Sesión eliminada con éxito")
    return redirect('session_list')


# ########################################################
# Semestre
# ########################################################

@login_required
@lecturer_required
def semester_list_view(request):
    """
    Vista para mostrar la lista de todos los semestres.
    """
    semesters = Semester.objects.all().order_by('-is_current_semester', '-semester')
    return render(request, 'app/semester_list.html', {"semesters": semesters, })


@login_required
@lecturer_required
def semester_add_view(request):
    """
    Vista para agregar un nuevo semestre.
    """
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            data = form.data.get('is_current_semester')  # devuelve una cadena 'True' si el usuario seleccionó Sí
            if data == 'True':
                semester = form.data.get('semester')
                ss = form.data.get('session')
                session = Session.objects.get(pk=ss)
                try:
                    if Semester.objects.get(semester=semester, session=ss):
                        messages.error(request, semester + " semestre en " + session.session + " sesión ya existe")
                        return redirect('add_semester')
                except:
                    semesters = Semester.objects.all()
                    sessions = Session.objects.all()
                    if semesters:
                        for semester in semesters:
                            if semester.is_current_semester == True:
                                unset_semester = Semester.objects.get(is_current_semester=True)
                                unset_semester.is_current_semester = False
                                unset_semester.save()
                        for session in sessions:
                            if session.is_current_session == True:
                                unset_session = Session.objects.get(is_current_session=True)
                                unset_session.is_current_session = False
                                unset_session.save()
                    new_session = request.POST.get('session')
                    set_session = Session.objects.get(pk=new_session)
                    set_session.is_current_session = True
                    set_session.save()
                    form.save()
                    messages.success(request, 'Semestre añadido con éxito.')
                    return redirect('semester_list')
            form.save()
            messages.success(request, 'Semestre añadido con éxito.')
            return redirect('semester_list')
    else:
        form = SemesterForm()
    return render(request, 'app/semester_update.html', {'form': form})


@login_required
@lecturer_required
def semester_update_view(request, pk):
    """
    Vista para actualizar un semestre existente.
    """
    semester = Semester.objects.get(pk=pk)
    if request.method == 'POST':
        if request.POST.get('is_current_semester') == 'True':
            unset_semester = Semester.objects.get(is_current_semester=True)
            unset_semester.is_current_semester = False
            unset_semester.save()
            unset_session = Session.objects.get(is_current_session=True)
            unset_session.is_current_session = False
            unset_session.save()
            new_session = request.POST.get('session')
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                set_session = Session.objects.get(pk=new_session)
                set_session.is_current_session = True
                set_session.save()
                form.save()
                messages.success(request, '¡Semestre actualizado con éxito!')
                return redirect('semester_list')
        else:
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                form.save()
                return redirect('semester_list')
    else:
        form = SemesterForm(instance=semester)
    return render(request, 'app/semester_update.html', {'form': form})


@login_required
@lecturer_required
def semester_delete_view(request, pk):
    """
    Vista para eliminar un semestre existente.
    """
    semester = get_object_or_404(Semester, pk=pk)
    if semester.is_current_semester:
        messages.error(request, "No puede eliminar el semestre actual")
        return redirect('semester_list')
    else:
        semester.delete()
        messages.success(request, "Semestre eliminado con éxito")
    return redirect('semester_list')


@login_required
@admin_required
def dashboard_view(request):
    """
    Vista para mostrar el panel de control del administrador.
    """
    return render(request, 'app/dashboard.html')

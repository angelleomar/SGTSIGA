from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic import CreateView, ListView
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from .decorators import lecturer_required, student_required, admin_required
from course.models import Course
from result.models import TakenCourse
from app.models import Session, Semester
from .forms import StaffAddForm, StudentAddForm, ProfileUpdateForm, ParentAddForm
from .models import User, Student, Parent


def validate_username(request):
    """
    Vista que valida si un nombre de usuario está disponible o no.
    Se utiliza para la verificación en tiempo real de la disponibilidad del nombre de usuario durante el registro.
    """
    username = request.GET.get("username", None)
    data = {
        "is_taken": User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def register(request):
    """
    Vista para el registro de usuarios.
    Permite a los usuarios registrarse como estudiantes.
    """
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente.')
        else:
            messages.error(request, 'Algo no está correcto, por favor completa todos los campos correctamente.')
    else:
        form = StudentAddForm(request.POST)
    return render(request, "registration/register.html", {'form': form})


@login_required
def profile(request):
    """Mostrar el perfil de cualquier usuario que realice la solicitud"""
    try:
        current_session = get_object_or_404(Session, is_current_session=True)
        current_semester = get_object_or_404(Semester, is_current_semester=True, session=current_session)
    except Semester.MultipleObjectsReturned and Semester.DoesNotExist and Session.DoesNotExist:
        raise Http404

    if request.user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id).filter(
            semester=current_semester)
        return render(request, 'accounts/profile.html', {
            'Titulo': request.user.get_full_name,
            "courses": courses,
            'current_session': current_session,
            'current_semester': current_semester,
        })
    elif request.user.is_student:
        level = Student.objects.get(student__pk=request.user.id)
        try:
            parent = Parent.objects.get(student=level)
        except:
            parent = "sin padre asignado"
        courses = TakenCourse.objects.filter(student__student__id=request.user.id, course__level=level.level)
        context = {
            'Titulo': request.user.get_full_name,
            'parent': parent,
            'courses': courses,
            'level': level,
            'current_session': current_session,
            'current_semester': current_semester,
        }
        return render(request, 'accounts/profile.html', context)
    else:
        staff = User.objects.filter(is_lecturer=True)
        return render(request, 'accounts/profile.html', {
            'Titulo': request.user.get_full_name,
            "staff": staff,
            'current_session': current_session,
            'current_semester': current_semester,
        })


@login_required
def profile_single(request, id):
    """Mostrar el perfil de un usuario seleccionado"""
    if request.user.id == id:
        return redirect("/profile/")

    current_session = get_object_or_404(Session, is_current_session=True)
    current_semester = get_object_or_404(Semester, is_current_semester=True, session=current_session)
    user = User.objects.get(pk=id)
    if user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=id).filter(semester=current_semester)
        context = {
            'Titulo': user.get_full_name,
            "user": user,
            "user_type": "Lecturer",
            "courses": courses,
            'current_session': current_session,
            'current_semester': current_semester,
        }
        return render(request, 'accounts/profile_single.html', context)
    elif user.is_student:
        student = Student.objects.get(student__pk=id)
        courses = TakenCourse.objects.filter(student__student__id=id, course__level=student.level)
        context = {
            'Titulo': user.get_full_name,
            'user': user,
            "user_type": "Estudiante",
            'courses': courses,
            'student': student,
            'current_session': current_session,
            'current_semester': current_semester,
        }
        return render(request, 'accounts/profile_single.html', context)
    else:
        context = {
            'Titulo': user.get_full_name,
            "user": user,
            "user_type": "superuser",
            'current_session': current_session,
            'current_semester': current_semester,
        }
        return render(request, 'accounts/profile_single.html', context)


@login_required
@admin_required
def admin_panel(request):
    """
    Vista del panel de administración para el administrador.
    """
    return render(request, 'setting/admin_panel.html', {})


@login_required
def profile_update(request):
    """
    Vista para actualizar el perfil del usuario.
    Permite al usuario actualizar su información personal.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrige el(los) error(es) a continuación.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'setting/profile_info_change.html', {
        'Titulo': 'Configuración | DjangoSMS',
        'form': form,
    })


@login_required
def change_password(request):
    """
    Vista para cambiar la contraseña del usuario.
    Permite al usuario cambiar su contraseña actual por una nueva.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '¡Tu contraseña se ha actualizado correctamente!')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrige el(los) error(es) a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'setting/password_change.html', {
        'form': form,
    })


@login_required
@admin_required
def staff_add_view(request):
    """
    Vista para agregar personal (lecturer) al sistema.
    Permite al administrador agregar nuevos lecturers.
    """
    if request.method == 'POST':
        form = StaffAddForm(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha creado la cuenta para el profesor " + first_name + ' ' + last_name + ".")
            return redirect("lecturer_list")
    else:
        form = StaffAddForm()

    context = {
        'Titulo': 'Agregar Profesor | DjangoSMS',
        'form': form,
    }

    return render(request, 'accounts/add_staff.html', context)


@login_required
@admin_required
def edit_staff(request, pk):
    """
    Vista para editar el perfil de un lecturer.
    Permite al administrador editar la información personal de un lecturer.
    """
    instance = get_object_or_404(User, is_lecturer=True, pk=pk)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
        full_name = instance.get_full_name
        if form.is_valid():
            form.save()

            messages.success(request, 'Se ha actualizado el perfil del profesor ' + full_name + '.')
            return redirect('lecturer_list')
        else:
            messages.error(request, 'Por favor corrige el(los) error(es) a continuación.')
    else:
        form = ProfileUpdateForm(instance=instance)
    return render(request, 'accounts/edit_lecturer.html', {
        'Titulo': 'Editar Profesor | DjangoSMS',
        'form': form,
    })


@method_decorator([login_required, admin_required], name='dispatch')
class LecturerListView(ListView):
    """
    Vista de lista de lecturers para el administrador.
    Muestra una lista de todos los lecturers registrados en el sistema.
    """
    queryset = User.objects.filter(is_lecturer=True)
    template_name = "accounts/lecturer_list.html"
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Titulo'] = "Profesores | DjangoSMS"
        return context


@login_required
@admin_required
def delete_staff(request, pk):
    """
    Vista para eliminar a un lecturer.
    Permite al administrador eliminar un lecturer del sistema.
    """
    lecturer = get_object_or_404(User, pk=pk)
    full_name = lecturer.get_full_name
    lecturer.delete()
    messages.success(request, 'Se ha eliminado al profesor ' + full_name + '.')
    return redirect('lecturer_list')


@login_required
@admin_required
def student_add_view(request):
    """
    Vista para agregar estudiantes al sistema.
    Permite al administrador agregar nuevos estudiantes.
    """
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha creado la cuenta para ' + first_name + ' ' + last_name + '.')
            return redirect('student_list')
        else:
            messages.error(request, 'Corrige el(los) error(es) a continuación.')
    else:
        form = StudentAddForm()

    return render(request, 'accounts/add_student.html', {
        'Titulo': "Agregar Estudiante | DjangoSMS",
        'form': form
    })


@login_required
@admin_required
def edit_student(request, pk):
    """
    Vista para editar el perfil de un estudiante.
    Permite al administrador editar la información personal de un estudiante.
    """
    instance = get_object_or_404(User, is_student=True, pk=pk)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
        full_name = instance.get_full_name
        if form.is_valid():
            form.save()

            messages.success(request, ('Se ha actualizado el perfil del estudiante ' + full_name + '.'))
            return redirect('student_list')
        else:
            messages.error(request, 'Por favor corrige el(los) error(es) a continuación.')
    else:
        form = ProfileUpdateForm(instance=instance)
    return render(request, 'accounts/edit_student.html', {
        'Titulo': 'Editar Estudiante | DjangoSMS',
        'form': form,
    })


@method_decorator([login_required, admin_required], name='dispatch')
class StudentListView(ListView):
    """
    Vista de lista de estudiantes para el administrador.
    Muestra una lista de todos los estudiantes registrados en el sistema.
    """
    template_name = "accounts/student_list.html"
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        queryset = Student.objects.all()
        query = self.request.GET.get('student_id')
        if query is not None:
            queryset = queryset.filter(Q(department=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Titulo'] = "Estudiantes | DjangoSMS"
        return context


@login_required
@admin_required
def delete_student(request, pk):
    """
    Vista para eliminar a un estudiante.
    Permite al administrador eliminar un estudiante del sistema.
    """
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, 'Se ha eliminado al estudiante.')
    return redirect('student_list')


class ParentAdd(CreateView):
    """
    Vista para agregar padres al sistema.
    Permite al administrador agregar nuevos padres.
    """
    model = Parent
    form_class = ParentAddForm
    template_name = 'accounts/parent_form.html'

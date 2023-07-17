from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Avg, Max, Min, Count
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from accounts.models import User, Student
from app.models import Session, Semester
from result.models import TakenCourse
from accounts.decorators import lecturer_required, student_required
from .forms import (
    ProgramForm, CourseAddForm, CourseAllocationForm, 
    EditCourseAllocationForm, UploadFormFile, UploadFormVideo
)
from .models import Program, Course, CourseAllocation, Upload, UploadVideo


# ########################################################
# Vistas de programas (Program views)
# ########################################################

@login_required
def program_view(request):
    """
    Vista que muestra la lista de programas.
    Los programas se pueden filtrar por título utilizando el parámetro 'program_filter' en la URL.
    """
    programs = Program.objects.all()

    program_filter = request.GET.get('program_filter')
    if program_filter:
        programs = Program.objects.filter(Titulo__icontains=program_filter)

    return render(request, 'course/program_list.html', {
        'Titulo': "Programas | DjangoSMS",
        'programs': programs,
    })


@login_required
@lecturer_required
def program_add(request):
    """
    Vista para agregar un nuevo programa.
    Se utiliza el formulario ProgramForm para recopilar los datos del programa.
    """
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, request.POST.get('Titulo') + ' programa ha sido creado.')
            return redirect('programs')
        else:
            messages.error(request, 'Corrige el/los error(es) a continuación.')
    else:
        form = ProgramForm()

    return render(request, 'course/program_add.html', {
        'Titulo': "Agregar Programa | DjangoSMS",
        'form': form,
    })


@login_required
def program_detail(request, pk):
    """
    Vista que muestra los detalles de un programa específico y los cursos asociados a ese programa.
    Los cursos se paginan para mostrar solo una cantidad determinada por página.
    """
    program = Program.objects.get(pk=pk)
    courses = Course.objects.filter(program_id=pk).order_by('-year')
    credits = Course.objects.aggregate(Sum('credit'))

    paginator = Paginator(courses, 10)
    page = request.GET.get('page')

    courses = paginator.get_page(page)

    return render(request, 'course/program_single.html', {
        'Titulo': program.Titulo,
        'program': program, 'courses': courses, 'credits': credits
    })


@login_required
@lecturer_required
def program_edit(request, pk):
    """
    Vista para editar un programa existente.
    Se utiliza el formulario ProgramForm para recopilar los datos actualizados del programa.
    """
    program = Program.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, str(request.POST.get('Titulo')) + ' programa ha sido actualizado.')
            return redirect('programs')
    else:
        form = ProgramForm(instance=program)

    return render(request, 'course/program_add.html', {
        'Titulo': "Editar Programa | DjangoSMS",
        'form': form
    })


@login_required
@lecturer_required
def program_delete(request, pk):
    """
    Vista para eliminar un programa existente.
    Se elimina el programa y se muestra un mensaje de éxito.
    """
    program = Program.objects.get(pk=pk)
    Titulo = program.Titulo
    program.delete()
    messages.success(request, 'Programa ' + Titulo + ' ha sido eliminado.')

    return redirect('programs')
# ########################################################


# ########################################################
# Vistas de cursos (Course views)
# ########################################################

@login_required
def course_single(request, slug):
    """
    Vista que muestra los detalles de un curso específico, incluidos los archivos y videos asociados a ese curso.
    """
    course = Course.objects.get(slug=slug)
    files = Upload.objects.filter(course__slug=slug)
    videos = UploadVideo.objects.filter(course__slug=slug)

    lecturers = CourseAllocation.objects.filter(courses__pk=course.id)

    return render(request, 'course/course_single.html', {
        'Titulo': course.Titulo,
        'course': course,
        'files': files,
        'videos': videos,
        'lecturers': lecturers,
        'media_url': settings.MEDIA_ROOT,
    })


@login_required
@lecturer_required
def course_add(request, pk):
    """
    Vista para agregar un nuevo curso a un programa existente.
    Se utiliza el formulario CourseAddForm para recopilar los datos del curso.
    """
    users = User.objects.all()
    if request.method == 'POST':
        form = CourseAddForm(request.POST)
        course_name = request.POST.get('Titulo')
        course_code = request.POST.get('code')
        if form.is_valid():
            form.save()
            messages.success(request, (course_name + '(' + course_code + ')' + ' ha sido creado.'))
            return redirect('program_detail', pk=request.POST.get('program'))
        else:
            messages.error(request, 'Corrige el/los error(es) a continuación.')
    else:
        form = CourseAddForm(initial={'program': Program.objects.get(pk=pk)})

    return render(request, 'course/course_add.html', {
        'Titulo': "Agregar Curso | DjangoSMS",
        'form': form, 'program': pk, 'users': users
    })


@login_required
@lecturer_required
def course_edit(request, slug):
    """
    Vista para editar un curso existente.
    Se utiliza el formulario CourseAddForm para recopilar los datos actualizados del curso.
    """
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseAddForm(request.POST, instance=course)
        course_name = request.POST.get('Titulo')
        course_code = request.POST.get('code')
        if form.is_valid():
            form.save()
            messages.success(request, (course_name + '(' + course_code + ')' + ' ha sido actualizado.'))
            return redirect('program_detail', pk=request.POST.get('program'))
        else:
            messages.error(request, 'Corrige el/los error(es) a continuación.')
    else:
        form = CourseAddForm(instance=course)

    return render(request, 'course/course_add.html', {
        'Titulo': "Editar Curso | DjangoSMS",
        'form': form
    })


@login_required
@lecturer_required
def course_delete(request, slug):
    """
    Vista para eliminar un curso existente.
    Se elimina el curso y se muestra un mensaje de éxito.
    """
    course = Course.objects.get(slug=slug)
    course.delete()
    messages.success(request, 'Curso ' + course.Titulo + ' ha sido eliminado.')

    return redirect('program_detail', pk=course.program.id)
# ########################################################


# ########################################################
# Asignación de cursos (Course Allocation)
# ########################################################

@method_decorator([login_required], name='dispatch')
class CourseAllocationFormView(CreateView):
    """
    Vista basada en clase que muestra un formulario para asignar cursos a un profesor.
    Utiliza el formulario CourseAllocationForm para recopilar los datos de asignación.
    """
    form_class = CourseAllocationForm
    template_name = 'course/course_allocation_form.html'

    def get_form_kwargs(self):
        kwargs = super(CourseAllocationFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        lecturer = form.cleaned_data['lecturer']
        selected_courses = form.cleaned_data['courses']
        courses = ()
        for course in selected_courses:
            courses += (course.pk,)
        try:
            a = CourseAllocation.objects.get(lecturer=lecturer)
        except:
            a = CourseAllocation.objects.create(lecturer=lecturer)
        for i in range(0, selected_courses.count()):
            a.courses.add(courses[i])
            a.save()
        return redirect('course_allocation_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Titulo'] = "Asignar Curso | DjangoSMS"
        return context


@login_required
def course_allocation_view(request):
    """
    Vista que muestra la lista de cursos asignados a profesores.
    """
    allocated_courses = CourseAllocation.objects.all()
    return render(request, 'course/course_allocation_view.html', {
        'Titulo': "Asignación de Cursos | DjangoSMS",
        "allocated_courses": allocated_courses
    })


@login_required
@lecturer_required
def edit_allocated_course(request, pk):
    """
    Vista para editar un curso asignado a un profesor.
    Se utiliza el formulario EditCourseAllocationForm para recopilar los datos actualizados de la asignación.
    """
    allocated = get_object_or_404(CourseAllocation, pk=pk)
    if request.method == 'POST':
        form = EditCourseAllocationForm(request.POST, instance=allocated)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignación de curso actualizada.')
            return redirect('course_allocation_view')
    else:
        form = EditCourseAllocationForm(instance=allocated)

    return render(request, 'course/course_allocation_form.html', {
        'Titulo': "Editar Curso Asignado | DjangoSMS",
        'form': form, 'allocated': pk
    })


@login_required
@lecturer_required
def deallocate_course(request, pk):
    """
    Vista para desasignar un curso asignado a un profesor.
    Se elimina la asignación y se muestra un mensaje de éxito.
    """
    course = CourseAllocation.objects.get(pk=pk)
    course.delete()
    messages.success(request, '¡Desasignado exitosamente!')
    return redirect("course_allocation_view")
# ########################################################


# ########################################################
# Vistas de carga de archivos (File Upload views)
# ########################################################

@login_required
@lecturer_required
def handle_file_upload(request, slug):
    """
    Vista para manejar la carga de archivos para un curso específico.
    Se utiliza el formulario UploadFormFile para recopilar los datos del archivo.
    """
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES, {'course': course})
        if form.is_valid():
            form.save()
            messages.success(request, (request.POST.get('Titulo') + ' ha sido subido.'))
            return redirect('course_detail', slug=slug)
    else:
        form = UploadFormFile()
    return render(request, 'upload/upload_file_form.html', {
        'Titulo': "Cargar Archivo | DjangoSMS",
        'form': form, 'course': course
    })


@login_required
@lecturer_required
def handle_file_edit(request, slug, file_id):
    """
    Vista para editar un archivo cargado para un curso específico.
    Se utiliza el formulario UploadFormFile para recopilar los datos actualizados del archivo.
    """
    course = Course.objects.get(slug=slug)
    instance = Upload.objects.get(pk=file_id)
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, (request.POST.get('Titulo') + ' ha sido actualizado.'))
            return redirect('course_detail', slug=slug)
    else:
        form = UploadFormFile(instance=instance)

    return render(request, 'upload/upload_file_form.html', {
        'Titulo': instance.Titulo,
        'form': form, 'course': course})


def handle_file_delete(request, slug, file_id):
    """
    Vista para eliminar un archivo cargado para un curso específico.
    Se elimina el archivo y se muestra un mensaje de éxito.
    """
    file = Upload.objects.get(pk=file_id)
    file.delete()

    messages.success(request, (file.Titulo + ' ha sido eliminado.'))
    return redirect('course_detail', slug=slug)

# ########################################################
# Vistas de carga de videos (Video Upload views)
# ########################################################

@login_required
@lecturer_required
def handle_video_upload(request, slug):
    """
    Vista para manejar la carga de videos para un curso específico.
    Se utiliza el formulario UploadFormVideo para recopilar los datos del video.
    """
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        form = UploadFormVideo(request.POST, request.FILES, {'course': course})
        if form.is_valid():
            form.save()
            messages.success(request, (request.POST.get('Titulo') + ' ha sido subido.'))
            return redirect('course_detail', slug=slug)
    else:
        form = UploadFormVideo()
    return render(request, 'upload/upload_video_form.html', {
        'Titulo': "Cargar Video | DjangoSMS",
        'form': form, 'course': course
    })


@login_required
def handle_video_single(request, slug, video_slug):
    """
    Vista que muestra un video específico para un curso.
    """
    course = get_object_or_404(Course, slug=slug)
    video = get_object_or_404(UploadVideo, slug=video_slug)
    return render(request, 'upload/video_single.html', {'video': video})


@login_required
@lecturer_required
def handle_video_edit(request, slug, video_slug):
    """
    Vista para editar un video cargado para un curso específico.
    Se utiliza el formulario UploadFormVideo para recopilar los datos actualizados del video.
    """
    course = Course.objects.get(slug=slug)
    instance = UploadVideo.objects.get(slug=video_slug)
    if request.method == 'POST':
        form = UploadFormVideo(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, (request.POST.get('Titulo') + ' ha sido actualizado.'))
            return redirect('course_detail', slug=slug)
    else:
        form = UploadFormVideo(instance=instance)

    return render(request, 'upload/upload_video_form.html', {
        'Titulo': instance.Titulo,
        'form': form, 'course': course})


def handle_video_delete(request, slug, video_slug):
    """
    Vista para eliminar un video cargado para un curso específico.
    Se elimina el video y se muestra un mensaje de éxito.
    """
    video = get_object_or_404(UploadVideo, slug=video_slug)
    video.delete()

    messages.success(request, (video.Titulo + ' ha sido eliminado.'))
    return redirect('course_detail', slug=slug)
# ########################################################


# ########################################################
# Registro de cursos (Course Registration)
# ########################################################

@login_required
@student_required
def course_registration(request):
    """
    Vista para el registro de cursos por parte de un estudiante.
    Permite al estudiante registrar los cursos que desea tomar.
    También muestra los cursos ya registrados por el estudiante.
    """
    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # eliminar csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            student = Student.objects.get(student__pk=request.user.id)
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.create(student=student, course=course)
            obj.save()
            messages.success(request, '¡Cursos registrados exitosamente!')
        return redirect('course_registration')
    else:
        student = get_object_or_404(Student, student__id=request.user.id)
        taken_courses = TakenCourse.objects.filter(student__student__id=request.user.id)
        t = ()
        for i in taken_courses:
            t += (i.course.pk,)
        current_semester = Semester.objects.get(is_current_semester=True)

        courses = Course.objects.filter(program__pk=student.department.id, level=student.level, semester=current_semester
        ).exclude(id__in=t).order_by('year')
        all_courses = Course.objects.filter(level=student.level, program__pk=student.department.id)

        no_course_is_registered = False  # Verificar si no hay cursos registrados
        all_courses_are_registered = False

        registered_courses = Course.objects.filter(level=student.level).filter(id__in=t)
        if registered_courses.count() == 0:  # Verificar si el número de cursos registrados es 0
            no_course_is_registered = True

        if registered_courses.count() == all_courses.count():
            all_courses_are_registered = True

        total_first_semester_credit = 0
        total_sec_semester_credit = 0
        total_registered_credit = 0
        for i in courses:
            if i.semester == "First":
                total_first_semester_credit += int(i.credit)
            if i.semester == "Second":
                total_sec_semester_credit += int(i.credit)
        for i in registered_courses:
            total_registered_credit += int(i.credit)
        context = {
            "is_calender_on": True,
            "all_courses_are_registered": all_courses_are_registered,
            "no_course_is_registered": no_course_is_registered,
            "current_semester": current_semester,
            "courses": courses,
            "total_first_semester_credit": total_first_semester_credit,
            "total_sec_semester_credit": total_sec_semester_credit,
            "registered_courses": registered_courses,
            "total_registered_credit": total_registered_credit,
            "student": student,
        }
        return render(request, 'course/course_registration.html', context)


@login_required
@student_required
def course_drop(request):
    """
    Vista para eliminar un curso registrado por un estudiante.
    Se elimina el curso y se muestra un mensaje de éxito.
    """
    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # eliminar csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            student = Student.objects.get(student__pk=request.user.id)
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.get(student=student, course=course)
            obj.delete()
            messages.success(request, '¡Eliminado exitosamente!')
        return redirect('course_registration')
# ########################################################


@login_required
def user_course_list(request):
    """
    Vista que muestra la lista de cursos asociados al usuario actual.
    Si el usuario es un profesor, muestra los cursos que se le han asignado.
    Si el usuario es un estudiante, muestra los cursos que ha registrado.
    """
    if request.user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id)

        return render(request, 'course/user_course_list.html', {'courses': courses})

    elif request.user.is_student:
        student = Student.objects.get(student__pk=request.user.id)
        taken_courses = TakenCourse.objects.filter(student__student__id=student.student.id)
        courses = Course.objects.filter(level=student.level).filter(program__pk=student.department.id)

        return render(request, 'course/user_course_list.html', {
            'student': student,
            'taken_courses': taken_courses,
            'courses': courses
        })

    else:
        return render(request, 'course/user_course_list.html')

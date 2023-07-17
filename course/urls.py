from django.urls import path
from .views import *


urlpatterns = [
    # URLs para los programas
    path('', program_view, name='programs'),
    path('<int:pk>/detail/', program_detail, name='program_detail'),
    path('add/', program_add, name='add_program'),
    path('<int:pk>/edit/', program_edit, name='edit_program'),
    path('<int:pk>/delete/', program_delete, name='program_delete'),

    # URLs para los cursos
    path('course/<slug>/detail/', course_single, name='course_detail'),
    path('<int:pk>/course/add/', course_add, name='course_add'),
    path('course/<slug>/edit/', course_edit, name='edit_course'),
    path('course/delete/<slug>/', course_delete, name='delete_course'),

    # URLs para la asignación de cursos
    path('course/assign/', CourseAllocationFormView.as_view(), name='course_allocation'),
    path('course/allocated/', course_allocation_view, name='course_allocation_view'),
    path('allocated_course/<int:pk>/edit/', edit_allocated_course, name='edit_allocated_course'),
    path('course/<int:pk>/deallocate/', deallocate_course, name='course_deallocate'),

    # URLs para la carga de archivos
    path('course/<slug>/documentations/upload/', handle_file_upload, name='upload_file_view'),
    path('course/<slug>/documentations/<int:file_id>/edit/', handle_file_edit, name='upload_file_edit'),
    path('course/<slug>/documentations/<int:file_id>/delete/', handle_file_delete, name='upload_file_delete'),

    # URLs para la carga de videos
    path('course/<slug>/video_tutorials/upload/', handle_video_upload, name='upload_video'),
    path('course/<slug>/video_tutorials/<video_slug>/detail/', handle_video_single, name='video_single'),
    path('course/<slug>/video_tutorials/<video_slug>/edit/', handle_video_edit, name='upload_video_edit'),
    path('course/<slug>/video_tutorials/<video_slug>/delete/', handle_video_delete, name='upload_video_delete'),

    # URLs para el registro de cursos
    path('course/registration/', course_registration, name='course_registration'),
    path('course/drop/', course_drop, name='course_drop'),
    
    # URL para la lista de cursos del usuario
    path('my_courses/', user_course_list, name="user_course_list"),
]

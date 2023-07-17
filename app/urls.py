from django.urls import path
from .views import (
    home_view, post_add, edit_post, delete_post,
    session_list_view, session_add_view, session_update_view, session_delete_view,
    semester_list_view, semester_add_view, semester_update_view, semester_delete_view,
    dashboard_view
)

urlpatterns = [
    # Página de inicio
    path('', home_view, name='home'),

    # Agregar publicación
    path('add_item/', post_add, name='add_item'),

    # Editar publicación
    path('item/<int:pk>/edit/', edit_post, name='edit_post'),

    # Eliminar publicación
    path('item/<int:pk>/delete/', delete_post, name='delete_post'),

    # Lista de sesiones
    path('session/', session_list_view, name="session_list"),

    # Agregar sesión
    path('session/add/', session_add_view, name="add_session"),

    # Editar sesión
    path('session/<int:pk>/edit/', session_update_view, name="edit_session"),

    # Eliminar sesión
    path('session/<int:pk>/delete/', session_delete_view, name="delete_session"),

    # Lista de semestres
    path('semester/', semester_list_view, name="semester_list"),

    # Agregar semestre
    path('semester/add/', semester_add_view, name="add_semester"),

    # Editar semestre
    path('semester/<int:pk>/edit/', semester_update_view, name="edit_semester"),

    # Eliminar semestre
    path('semester/<int:pk>/delete/', semester_delete_view, name="delete_semester"),

    # Panel de control
    path('dashboard/', dashboard_view, name="dashboard"),
]

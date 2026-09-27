from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='task/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),

    path('subtasks/', views.subtask_list, name='subtask_list'),
    path('subtasks/create/', views.subtask_create, name='subtask_create'),
    path('subtasks/<int:pk>/edit/', views.subtask_update, name='subtask_update'),
    path('subtasks/<int:pk>/delete/', views.subtask_delete, name='subtask_delete'),

    path('notes/', views.note_list, name='note_list'),
    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/edit/', views.note_update, name='note_update'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('priorities/', views.priority_list, name='priority_list'),
    path('priorities/create/', views.priority_create, name='priority_create'),
    path('priorities/<int:pk>/edit/', views.priority_update, name='priority_update'),
    path('priorities/<int:pk>/delete/', views.priority_delete, name='priority_delete'),
]

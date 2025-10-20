from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    PriorityListView, PriorityCreateView, PriorityUpdateView, PriorityDeleteView,
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    SubTaskListView, SubTaskCreateView, SubTaskUpdateView, SubTaskDeleteView,
    NoteListView, NoteCreateView, NoteUpdateView, NoteDeleteView,
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    # Priorities
    path('priorities/', PriorityListView.as_view(), name='priority-list'),
    path('priorities/add/', PriorityCreateView.as_view(), name='priority-add'),
    path('priorities/<int:pk>/edit/', PriorityUpdateView.as_view(), name='priority-edit'),
    path('priorities/<int:pk>/delete/', PriorityDeleteView.as_view(), name='priority-delete'),

    # Tasks
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/add/', TaskCreateView.as_view(), name='task-add'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-edit'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),

    # SubTasks
    path('subtasks/', SubTaskListView.as_view(), name='subtask-list'),
    path('subtasks/add/', SubTaskCreateView.as_view(), name='subtask-add'),
    path('subtasks/<int:pk>/edit/', SubTaskUpdateView.as_view(), name='subtask-edit'),
    path('subtasks/<int:pk>/delete/', SubTaskDeleteView.as_view(), name='subtask-delete'),

    # Notes
    path('notes/', NoteListView.as_view(), name='note-list'),
    path('notes/add/', NoteCreateView.as_view(), name='note-add'),
    path('notes/<int:pk>/edit/', NoteUpdateView.as_view(), name='note-edit'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='socialaccount/login'), name='logout'),

]

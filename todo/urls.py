from django.urls import path
from . import views

urlpatterns = [
    path('todo/', views.get_todos, name='get-todos'),
    path('todo/create/', views.create_todo, name='create-todo'),
    path('todos/<str:pk>/', views.get_todo_detail, name='todo-detail'),
    path('todos/<str:pk>/update/', views.update_todo, name='update-todo-full'),  # PUT
    path('todos/<str:pk>/delete/', views.delete_todo, name='delete-todo'),
    path('todos/<str:pk>/mark-done/', views.mark_todo_done, name='mark-done'),  # PATCH
    path('todos/<str:pk>/toggle/', views.toggle_todo_status, name='toggle-todo'),
]
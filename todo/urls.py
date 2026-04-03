from django.urls import path
from . import views

urlpatterns = [
    path('todo/', views.get_todos, name='get-todos'),
    path('todo/create/', views.create_todo, name='create-todo'),
    path('todo/<str:pk>/', views.get_todo_detail, name='todo-detail'),
    path('todo/<str:pk>/update/', views.update_todo, name='update-todo-full'),  # PUT
    path('todo/<str:pk>/delete/', views.delete_todo, name='delete-todo'),
    path('todo/<str:pk>/mark-done/', views.mark_todo_done, name='mark-done'),  # PATCH
    path('todo/<str:pk>/toggle/', views.toggle_todo_status, name='toggle-todo'),
]
from django.urls import path
from .views import get_todos

urlpatterns = [
    path('todo/', get_todos),
]
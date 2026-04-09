from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register-user'),
    path('login', views.login_view, name='login-user')
]
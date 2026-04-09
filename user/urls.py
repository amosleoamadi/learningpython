from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register-user'),
    path('login', views.login_view, name='login-user'),
    path('verify-email', views.verify_email, name='verify-user'),
    path('resend-otp', views.resend_otp, name='resend-otp'),
    path('forgot-password', views.forgot_password, name='forget_password'),
    path('reset-password', views.reset_password, name='reset-password'),
]
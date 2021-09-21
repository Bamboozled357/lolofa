from django.urls import path
from .views import (RegistrationView, ActivationView, LoginView)

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register-account'),
    path('activate/', ActivationView.as_view(), name='acc-activation'),
    path('login/', LoginView.as_view(), name='login-page'),
]
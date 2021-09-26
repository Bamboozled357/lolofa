from main import views

from .views import (RegistrationView, ActivationView, LoginView, LogoutView, ForgotPasswordCompleteView,
                    ChangePasswordView, ForgotPasswordView)


from knox import views as knox_views
from django.urls import path, include

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password/complete/', ForgotPasswordCompleteView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path("response/list/", views.ListResponseAPIView.as_view(), name="response_list"),
    path("response/create/", views.CreateResponseAPIView.as_view(), name="response_create"),
    path("response/update/<int:pk>/", views.UpdateAPIView.as_view(), name="update_response"),
    path("response/delete/<int:pk>/", views.DeleteResponseAPIView.as_view(), name="delete_response"),
]



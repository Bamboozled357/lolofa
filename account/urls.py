from main import views

from .views import (RegisterAPI, LoginAPI, ChangePasswordView)

from .views import RegisterAPI, LoginAPI

from knox import views as knox_views
from django.urls import path, include

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path("list/product/",views.ListProductAPIView.as_view(),name="product_list"),
    path("product/create/", views.CreateProductAPIView.as_view(),name="product_create"),
    path("product/update/<int:pk>/",views.UpdateAPIView.as_view(),name="update_product"),
    path("product/delete/<int:pk>/",views.DeleteProductAPIView.as_view(),name="delete_product"),
    path("response/list/",views.ListResponseAPIView.as_view(), name="response_list"),
    path("response/create/", views.CreateResponseAPIView.as_view(),name="response_create"),
    path("response/update/<int:pk>/",views.UpdateAPIView.as_view(),name="update_response"),
    path("response/delete/<int:pk>/",views.DeleteResponseAPIView.as_view(),name="delete_response"),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]



from django.urls import path

from main import views

urlpatterns = [
    path("", views.ListProductAPIView.as_view(), name="product_list"),
    path("product/create/", views.CreateProductAPIView.as_view(), name="product_create"),
    path("product/update/<int:pk>/", views.UpdateAPIView.as_view(), name="update_product"),
    path("product/delete/<int:pk>/", views.DeleteProductAPIView.as_view(), name="delete_product"),
    path("response/listing/", views.ListResponseAPIView.as_view(), name="response_list"),
    path("response/create/", views.CreateResponseAPIView.as_view(), name="response_create"),
    path("response/update/<int:pk>/", views.UpdateAPIView.as_view(), name="update_response"),
    path("response/delete/<int:pk>/", views.DeleteResponseAPIView.as_view(), name="delete_response")
]

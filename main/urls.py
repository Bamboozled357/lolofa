from django.urls import path
from .views import (ProductsListView,
                    ProductDetailsView,
                    CreateProductView,
                    UpdateProductView,
                    DeleteProductView)

urlpatterns = [
    path('Products/', ProductsListView.as_view()),
    path('Products/<int:pk>/', ProductDetailsView.as_view()),
    path('Products/create/', CreateProductView.as_view()),
    path('Products/update/<int:pk>/', UpdateProductView.as_view()),
    path('Products/delete/<int:pk>/', DeleteProductView.as_view()),
]
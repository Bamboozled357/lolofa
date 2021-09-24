from django.urls import path
from rest_framework.routers import DefaultRouter

from main import views

router = DefaultRouter()
router.register('', views.ProductViewSet)

urlpatterns = [
    path("product/list/",views.ListProductAPIView.as_view(),name="product_list"),
    path("product/create/", views.CreateProductAPIView.as_view(),name="product_create"),
    path("product/update/<int:pk>/",views.UpdateAPIView.as_view(),name="update_product"),
    path("product/delete/<int:pk>/",views.DeleteProductAPIView.as_view(),name="delete_product"),
    path("response/list/",views.ListResponseAPIView.as_view(),name="response_list"),
    path("response/create/", views.CreateResponseAPIView.as_view(),name="response_create"),
    path("response/update/<int:pk>/",views.UpdateAPIView.as_view(),name="update_response"),
    path("response/delete/<int:pk>/",views.DeleteResponseAPIView.as_view(),name="delete_response"),
    path("rate/", views.UserProductRelationView.as_view({'get':'user'})),
    path('like/',
         views.LikeView.as_view(),
         name='like'),
    path('get-likers/',
         views.GetLikersView.as_view(),
         name='get-likers'),
]


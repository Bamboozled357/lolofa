from django.urls import path
from rest_framework.routers import DefaultRouter

from main import views
from main.views import LikeListCreate

router = DefaultRouter()
router.register('', views.ProductViewSet)

urlpatterns = [

    path("list/", views.ListProductAPIView.as_view(), name="product_list"),
    path("filter/", views.FilterProductAPIView.as_view(), name="product_filter"),
    path("details/<int:pk>", views.DetailProductAPIView.as_view(), name="product_list"),
    path("create/", views.CreateProductAPIView.as_view(), name="product_create"),
    path("update/<int:pk>/", views.UpdateProductAPIView.as_view(), name="update_product"),
    path("delete/<int:pk>/", views.DeleteProductAPIView.as_view(), name="delete_product"),

    path("response/list/", views.ListResponseAPIView.as_view(), name="response_list"),
    path("response/create/", views.CreateResponseAPIView.as_view(), name="response_create"),
    path("response/update/<int:pk>/", views.UpdateAPIView.as_view(), name="update_response"),
    path("response/delete/<int:pk>/", views.DeleteResponseAPIView.as_view(), name="delete_response"),

    path("cart/create/", views.CreateCartAPIView.as_view(), name="cart_create"),
    path("cart/update/<int:pk>/", views.UpdateCartAPIView.as_view(), name="cart_update"),
    path("cart/delete/<int:pk>/", views.DeleteCartAPIView.as_view(), name="cart_delete"),


    # path("product/list/",views.ListProductAPIView.as_view(),name="product_list"),
    # path("product/create/", views.CreateProductAPIView.as_view(),name="product_create"),
    # path("product/update/<int:pk>/",views.UpdateAPIView.as_view(),name="update_product"),
    # path("product/delete/<int:pk>/",views.DeleteProductAPIView.as_view(),name="delete_product"),
    # path("response/list/",views.ListResponseAPIView.as_view(),name="response_list"),
    # path("response/create/", views.CreateResponseAPIView.as_view(),name="response_create"),
    # path("response/update/<int:pk>/",views.UpdateAPIView.as_view(),name="update_response"),
    # path("response/delete/<int:pk>/",views.DeleteResponseAPIView.as_view(),name="delete_response"),
    # path("rate/", views.UserProductRelationView.as_view({'get':'user'})),
    # path('like/', LikeListCreate.as_view(), name='post_likes'),
    # path("cart/", views.CartAPIView.as_view()),
]

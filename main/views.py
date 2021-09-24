from itertools import product

import django_filters
from django.shortcuts import render
from rest_framework import mixins, generics, filters, permissions

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from main.models import Product, Response, UserProductRelation
from main.pagination import CustomPagination, CustomLikersPagination
from main.permissions import IsAuthor, IsOwnerOrStaffOrReadOnly
from main.serializers import ProductDetailSerializer, ProductListSerializer, ResponseSerializer, NoteSerializer, \
    AuthorSerializers


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super(CustomSearchFilter, self).get_search_fields(view, request)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ListProductAPIView(ListAPIView):
    """This endpoint list all of the available products from the database"""
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class CreateProductAPIView(CreateAPIView):
    """This endpoint allows for creation of a product"""
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class UpdateProductAPIView(UpdateAPIView):
    """This endpoint allows for updating a specific product by passing in the id of the product to update"""
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class DeleteProductAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific Todo from the database"""
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class ListResponseAPIView(ListAPIView):
    """This endpoint list all of the available todos from the database"""
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

class CreateResponseAPIView(CreateAPIView):
    """This endpoint allows for creation of a todo"""
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

class UpdateResponseAPIView(UpdateAPIView):
    """This endpoint allows for updating a specific todo by passing in the id of the todo to update"""
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

class DeleteResponseAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific Todo from the database"""
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class ResponseViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]


class UserProductRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProductRelation.objects.all()

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializers_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['price']
    search_fields = ['product', 'user']
    ordering_fields = ['price', 'user']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

#PAGINATION

from rest_framework.viewsets import ModelViewSet


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    pagination_class = CustomPagination

    def get_object(self):
        return get_object_or_404(Product, id=self.request.query_params.get("id"))

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('-last_udpated_on')

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()



class LikeView(ListAPIView):
    """Toggle like"""

    def get(self, request, format=None, product_id=None):
        post = Product.objects.get(pk=product_id)
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                like = False
                product.likes.remove(user)
            else:
                like = True
                product.likes.add(user)
        data = {
            'like': like
        }
        return Response(data)

class GetLikersView(generics.ListAPIView):
    serializer_class = AuthorSerializers
    pagination_class = CustomLikersPagination
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        product_id = self.kwargs['post_id']
        queryset = Product.objects.get(
            pk=product_id).likes.all()
        return queryset


from django.shortcuts import render
from rest_framework import mixins

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from main.models import Product, Response
from main.permissions import IsAuthor
from main.serializers import ProductDetailSerializer, ProductListSerializer, ResponseSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


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



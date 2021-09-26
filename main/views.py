from django.shortcuts import render
from rest_framework import mixins
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from main.models import (Product, Response)
from main.permissions import IsAuthor, IsAuthorOrIsAdmin
from main.serializers import (ListProductSerializer, DetailProductSerializer, ProductListSerializer,
                              ResponseSerializer, )


class ListProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer


class FilterProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer

    def get_queryset(self):
        """
        Эта вьюха должна возвращать список всех покупок текущего авторизованного пользователя
        """
        title = self.request.GET.get('title')
        queryset = super().get_queryset()
        queryset = queryset.filter(title__contains=title)
        return queryset


class CreateProductAPIView(CreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthorOrIsAdmin, ]


class DetailProductAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = DetailProductSerializer


class UpdateProductAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthorOrIsAdmin, ]


class DeleteProductAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthorOrIsAdmin, ]


class ListResponseAPIView(ListAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class CreateResponseAPIView(CreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class UpdateResponseAPIView(UpdateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class DeleteResponseAPIView(DestroyAPIView):
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

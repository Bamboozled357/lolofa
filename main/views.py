from itertools import product

import django_filters
from django.shortcuts import render
from rest_framework import mixins, generics, filters, permissions, status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from main.models import Product, Response, UserProductRelation
from main.pagination import CustomPagination
from main.permissions import IsAuthor, IsOwnerOrStaffOrReadOnly
from main.serializers import ProductDetailSerializer, ProductListSerializer, ResponseSerializer, CartSerializer, ProductlikeSerializer


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








class LikeView(generics.ListAPIView):
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



class CartAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = CartSerializer

class LikeListCreate(APIView):

    def get(self, request, pk):  # function to get total number of likes to particular post
        post = Product.objects.filter(pk=pk)  # find which post's likes are to be extracted
        like_count = post.likepost.count()  # counts total user likes ,besides my code is wrong
        serializer = ProductlikeSerializer(like_count, many=True)
        return Response(serializer.data)

    def post(self, request, pk):  # function to add likes to post
            # how do I check if user is already liked the post ?
        likeusers = request.user
        likepost = Product.objects.filter(pk=pk)
        serializer = ProductlikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(likeusers, likepost)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


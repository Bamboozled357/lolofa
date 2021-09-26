from itertools import product
import django_filters
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import mixins, generics, filters, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from main.models import (Product, Response)
from main.permissions import IsAuthor, IsAuthorOrIsAdmin
from main.serializers import (ListProductSerializer, DetailProductSerializer, ProductListSerializer,
                              ResponseSerializer, )
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from main.models import Product, Response, UserProductRelation
from main.pagination import CustomPagination
from main.permissions import IsAuthor, IsOwnerOrStaffOrReadOnly
from main.serializers import (DetailProductSerializer, ProductListSerializer,
                              ResponseSerializer, CartSerializer, ProductlikeSerializer)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super(CustomSearchFilter, self).get_search_fields(view, request)


class ListProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'


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

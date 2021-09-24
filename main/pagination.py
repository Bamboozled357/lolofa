from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2
    page_query_param = 'p'

class CustomLikersPagination(PageNumberPagination):
    page_size =10
    page_size_query_params = 'page_size'
    max_page_size = 100

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_params = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'links':{
                'next':self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count':self.page.paginator.count,
            'results':data
        })

class ResponsePagination(PageNumberPagination):
    page_size = 5
    page_size_query_params = 'page_size'
    max_page_size = 5

from rest_framework.pagination import PageNumberPagination


class MyCustomPaginator(PageNumberPagination):
    page_size_param = 'limit'

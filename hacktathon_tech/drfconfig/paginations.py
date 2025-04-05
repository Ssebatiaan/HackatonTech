from rest_framework import pagination


class CFEAPIPagination(pagination.LimitOffsetPagination):#pagination.PageNumberPagination):
    page_size = 2
    max_limit = 100
    default_limit = 100
    limit_query_param = 'limit'


class StandardResultsSetPagination(pagination.LimitOffsetPagination):
    page_size = 20
    max_limit = 10000
    default_limit = 20
    limit_query_param = 'limit'
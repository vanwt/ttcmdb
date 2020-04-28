from rest_framework.pagination import PageNumberPagination


class ALLPagination(PageNumberPagination):
    cursor_query_param = "cursor"
    max_page_size = 20
    page_size = 20
    page_size_query_param = "size"

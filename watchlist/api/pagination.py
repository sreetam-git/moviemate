from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class CustomPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 10
    last_page_strings = 'end'
    
class WatchlistLOPagination(LimitOffsetPagination):
    default_limit = 2
    
class WatchlistCPagination(CursorPagination):
    page_size = 2
    ordering = '-created_at'
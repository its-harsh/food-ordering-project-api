from rest_framework import pagination


class PageSize10Pagination(pagination.PageNumberPagination):
    page_size = 10

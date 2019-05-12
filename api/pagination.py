from collections import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response


class LimitedLimitOffsetPagination(pagination.LimitOffsetPagination):
    max_limit = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('results', data),
        ]))

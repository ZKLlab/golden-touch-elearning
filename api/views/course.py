from rest_framework import generics

import api.pagination
import api.permissions
import api.serializers
from course.models import Course


class CoursesView(generics.ListAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    pagination_class = api.pagination.LimitedLimitOffsetPagination
    serializer_class = api.serializers.course.CourseSerializer

    def get_queryset(self):
        return Course.objects.all()

import json
import math
import pytz
import datetime
from django.http import Http404
from django.conf import settings
from django.utils import timezone
from rest_framework import generics
from aliyunsdkcore.client import AcsClient
from rest_framework.response import Response
from aliyunsdkvod.request.v20170321 import GetVideoListRequest, GetPlayInfoRequest

import api.permissions
import api.serializers
from course.models import CourseCategory, Course, Lesson


def init_vod_client():
    return AcsClient(settings.ALIYUN_ACCESS_KEY_ID, settings.ALIYUN_ACCESS_KEY_SECRET, settings.ALIYUN_REGION_ID,
                     auto_retry=True, max_retry_time=settings.ALIYUN_MAX_RETRY_TIME,
                     timeout=settings.ALIYUN_CONNECT_TIMEOUT)


def get_video_list(clt, page_no, page_size):
    request = GetVideoListRequest.GetVideoListRequest()
    request.set_PageNo(page_no)
    request.set_PageSize(page_size)
    request.set_Status('Normal')
    request.set_accept_format('JSON')
    request.set_CateId(settings.ALIYUN_VOD_CATE_ID)
    response = json.loads(clt.do_action_with_exception(request))
    return response


def get_play_info(clt, video_id):
    request = GetPlayInfoRequest.GetPlayInfoRequest()
    request.set_accept_format('JSON')
    request.set_VideoId(video_id)
    request.set_AuthTimeout(3600 * 5)
    response = json.loads(clt.do_action_with_exception(request))
    return response


def seconds_to_duration(seconds):
    seconds = math.floor(seconds)
    ans = ''
    if seconds > 3600:
        ans += '{}小时'.format(seconds // 3600)
        seconds %= 3600
    if seconds > 60:
        ans += '{}分'.format(seconds // 60)
        seconds %= 60
    if seconds > 0:
        ans += '{}秒'.format(seconds)
    return ans


class CourseCategoriesView(generics.ListAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    serializer_class = api.serializers.course.CourseCategorySerializer

    def get_queryset(self):
        return CourseCategory.objects.all()


class CoursesView(generics.ListAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    serializer_class = api.serializers.course.CourseSerializer

    def get_queryset(self):
        return Course.objects.all()


class CourseView(generics.RetrieveUpdateDestroyAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    serializer_class = api.serializers.course.CourseSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Course.objects.all()


class CourseCreateView(generics.CreateAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    serializer_class = api.serializers.course.CourseCreateSerializer


class LessonsView(generics.ListAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    serializer_class = api.serializers.course.LessonSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            r = Course.objects.get(slug=slug)
        except Course.DoesNotExist:
            raise Http404
        return r.lessons.order_by('order')


class LessonCreateView(generics.CreateAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    serializer_class = api.serializers.course.LessonSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            r = Course.objects.get(slug=slug)
        except Course.DoesNotExist:
            raise Http404
        return r.lessons.order_by('order')


class LessonView(generics.RetrieveUpdateDestroyAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    serializer_class = api.serializers.course.LessonSerializer
    lookup_field = 'id'

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Lesson.objects.filter(course__slug=slug)


class VideosView(generics.ListAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)

    def get(self, request, *args, **kwargs):
        page_no = request.query_params.get('page_no', '1')
        limit = request.query_params.get('limit', '10')
        try:
            page_no = int(page_no)
        except ValueError:
            page_no = 0
        try:
            limit = int(limit)
        except ValueError:
            limit = 10
        if page_no < 1:
            page_no = 1
        if limit > 100:
            limit = 100
        clt = init_vod_client()
        response = get_video_list(clt, page_no, limit)
        results = []
        for video_info in response['VideoList']['Video']:
            creation_time = datetime.datetime.strptime(video_info['CreationTime'], '%Y-%m-%dT%H:%M:%SZ')
            creation_time = datetime.datetime(*creation_time.timetuple()[0:6], tzinfo=pytz.timezone('UTC'))
            results.append({
                'id': video_info['VideoId'],
                'title': video_info['Title'],
                'duration': seconds_to_duration(video_info.get('Duration', 0)),
                'creation_time': timezone.localtime(creation_time).strftime(u'%Y-%m-%d %H:%M:%S'),
                'cover': video_info.get('CoverURL', ''),
            })
        return Response({
            'count': response['Total'],
            'results': results,
        })


class PlayInfoView(generics.RetrieveAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)

    def get(self, request, *args, **kwargs):
        video_id = request.query_params.get('video_id', '')
        clt = init_vod_client()
        response = get_play_info(clt, video_id)
        return Response(response)

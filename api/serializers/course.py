import json
import traceback

from django.http import Http404
from django.conf import settings
from rest_framework import serializers
from aliyunsdkcore.client import AcsClient
from aliyunsdkvod.request.v20170321 import GetVideoInfoRequest

from course.models import CourseCategory, Course, Lesson


def init_vod_client():
    return AcsClient(settings.ALIYUN_ACCESS_KEY_ID, settings.ALIYUN_ACCESS_KEY_SECRET, settings.ALIYUN_REGION_ID,
                     auto_retry=True, max_retry_time=settings.ALIYUN_MAX_RETRY_TIME,
                     timeout=settings.ALIYUN_CONNECT_TIMEOUT)


def get_video_info(clt, video_id):
    request = GetVideoInfoRequest.GetVideoInfoRequest()
    request.set_VideoId(video_id)
    response = json.loads(clt.do_action_with_exception(request))
    return response


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = (
            'name',
        )


class CourseSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer()
    lessons_count = serializers.SerializerMethodField()
    category_name = serializers.CharField(write_only=True)

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()

    def update(self, instance, validated_data):
        if 'category_name' in validated_data:
            r = CourseCategory.objects.get_or_create(name=validated_data['category_name'])[0]
            o = instance.category
            instance.category = r
            instance.save()
            if o.courses.count() == 0:
                o.delete()
            del validated_data['category_name']
        super(CourseSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = Course
        fields = (
            'name', 'abbr', 'slug', 'visible', 'category', 'category_name', 'lessons_count'
        )


class CourseCreateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True)

    def create(self, validated_data):
        r = CourseCategory.objects.get_or_create(name=validated_data['category_name'])[0]
        return Course.objects.create(name=validated_data['name'], abbr=validated_data['abbr'],
                                     slug=validated_data['slug'], category=r)

    class Meta:
        model = Course
        fields = (
            'name', 'abbr', 'slug', 'category_name',
        )


class LessonSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    course_abbr = serializers.SerializerMethodField()
    course_slug = serializers.SerializerMethodField()
    video_cover = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    def create(self, validated_data):
        try:
            r = Course.objects.get(slug=self.context['view'].kwargs['slug'])
        except Course.DoesNotExist:
            raise Http404
        return Lesson.objects.create(course=r, order=r.lessons.count() + 1, **validated_data)

    @staticmethod
    def get_course_name(obj):
        return obj.course.name

    @staticmethod
    def get_course_abbr(obj):
        return obj.course.abbr

    @staticmethod
    def get_course_slug(obj):
        return obj.course.slug

    def get_video_cover(self, obj):
        if type(self.context['view']).__name__ == 'LessonView' and obj.video_id is not None:
            try:
                clt = init_vod_client()
                return get_video_info(clt, obj.video_id)['Video']['CoverURL']
            except Exception as err:
                print(err)
                traceback.print_exc()
                return ''
        else:
            return ''

    def get_lessons(self, obj):
        result = []
        if type(self.context['view']).__name__ == 'LessonView':
            r = obj.course.lessons.order_by('order')
            for item in r:
                result.append({
                    'id': item.id,
                    'name': item.name,
                    'order': item.order,
                })
        return result

    class Meta:
        model = Lesson
        fields = (
            'id', 'course', 'order', 'update_time', 'name', 'course_name', 'course_abbr', 'course_slug', 'lessons',
            'video_id', 'video_cover',
        )
        read_only_fields = (
            'id', 'course', 'update_time', 'order',
        )

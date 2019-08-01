import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver


class CourseCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)  # 名称


class Course(models.Model):
    name = models.CharField(max_length=150)  # 名称
    abbr = models.CharField(max_length=150, blank=True)  # 简称
    slug = models.SlugField(max_length=40, unique=True,
                            validators=[RegexValidator('^[a-z|-]*$'),
                                        RegexValidator('^([a-z][a-z|-]*[a-z]|[a-z])$')])  # slug
    visible = models.BooleanField(default=False)  # 可见性
    category = models.ForeignKey(CourseCategory, models.PROTECT, 'courses')  # 类别


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, models.CASCADE, 'lessons')
    order = models.IntegerField()
    update_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)  # 名称
    video_id = models.CharField(max_length=150, null=True, default=None)  # 阿里云视频ID


# noinspection PyUnusedLocal
@receiver(post_delete, sender=Lesson)
def lessons_reorder(sender, instance, **kwargs):
    lessons = sender.objects.filter(course=instance.course).order_by('order')
    for index, lesson in enumerate(lessons, 1):
        if lesson.order != index:
            lesson.order = index
            lesson.save()

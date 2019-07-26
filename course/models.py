from django.db import models


class CourseCategory(models.Model):
    name = models.CharField(max_length=150)  # 名称


class Course(models.Model):
    name = models.CharField(max_length=150)  # 名称
    abbr = models.CharField(max_length=150, blank=True)  # 简称
    slug = models.SlugField(max_length=40)  # slug
    visible = models.BooleanField(default=False)  # 可见性
    category = models.ForeignKey(CourseCategory, models.SET_NULL, 'courses', null=True, default=None)  # 类别

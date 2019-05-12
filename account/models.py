from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    display_name = models.CharField('显示名', max_length=150, db_index=True, blank=True)
    user_type = models.IntegerField('用户类别',  # 0: 学生, 1: 教师, 2: 志愿者
                                    validators=[MinValueValidator(0), MaxValueValidator(2)])
    gender = models.IntegerField('性别',  # 0: 未知, 1: 女, 2: 男
                                 validators=[MinValueValidator(0), MaxValueValidator(2)], default=0)
    phone_num = models.CharField('手机号', max_length=30, db_index=True, blank=True,
                                 validators=[RegexValidator(settings.REGEX_PHONE_NUM_ALLOW_BLANK)])

    @property
    def is_student(self):
        return self.user_type == 0

    @property
    def is_teacher(self):
        return self.user_type == 1

    @property
    def is_volunteer(self):
        return self.user_type == 2

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

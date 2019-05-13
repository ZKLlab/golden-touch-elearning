from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from account.models import User


class ChangePasswordSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())
    password = serializers.CharField()

    def create(self, validated_data):
        if self.context['request'].user.id in validated_data['ids']:
            msg = '不可重置当前权限用户的密码。'
            raise serializers.ValidationError(msg)
        try:
            with transaction.atomic():  # 原子操作，一个失败全部失败
                for _id in validated_data['ids']:
                    user = User.objects.get(id=_id)
                    user.set_password(validated_data['password'])
                    user.save()
                return {}
        except User.DoesNotExist:
            msg = '一个或多个用户不存在。'
            raise serializers.ValidationError(msg)

    def update(self, instance, validated_data):
        pass


class PasswordValidatorSerializer(serializers.Serializer):
    password = serializers.CharField()

    def create(self, validated_data):
        try:
            validate_password(validated_data['password'])
            return {'can_use': True}
        except ValidationError:
            return {'can_use': False}

    def update(self, instance, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.SerializerMethodField()
    has_password = serializers.SerializerMethodField()
    is_current_user = serializers.SerializerMethodField()

    @staticmethod
    def get_last_login(obj):
        if obj.last_login is not None:
            return timezone.localtime(obj.last_login).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return '/'

    @staticmethod
    def get_has_password(obj):
        return obj.password != ''

    def get_is_current_user(self, obj):
        return obj == self.context['request'].user

    class Meta:
        model = User
        fields = (
            'id', 'display_name', 'last_login', 'username', 'gender', 'is_superuser', 'is_active', 'is_current_user',
            'has_password',
        )
        read_only_fields = ('id', 'is_superuser', 'last_login', 'has_password')


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'display_name', 'user_type', 'last_login', 'username', 'gender', 'is_superuser',
        )

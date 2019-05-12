from django.contrib import auth
from rest_framework import serializers


class SessionSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password'),
        }

        if all(credentials.values()):
            user = auth.authenticate(**credentials)
            if user:
                if not user.is_active:
                    msg = '账号被禁用，请联系管理员！'
                    raise serializers.ValidationError(msg)
                auth.login(self.context['request'], user)
                return attrs
            else:
                msg = '用户名或密码错误！'
                raise serializers.ValidationError(msg)
        else:
            msg = '"username"和"password"是必填字段。'
            raise serializers.ValidationError(msg)

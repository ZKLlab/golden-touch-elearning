from django.http import Http404, HttpResponse
from rest_framework import generics
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password

import api.pagination
import api.permissions
import api.serializers
from account.models import User


class UsernameValidatorView(generics.GenericAPIView):
    """
    验证用户名是否可用
    """
    permission_classes = [api.permissions.IsSuperuser & api.permissions.IsVolunteer]

    @staticmethod
    def get(request):
        try:
            User.objects.get(username=request.query_params['u'])
            return Response({'can_use': False})
        except User.DoesNotExist:
            return Response({'can_use': True})
        except KeyError:
            return Response({'error': '"u"参数是必填项'}, status=400)


class PasswordValidatorView(generics.GenericAPIView):
    permission_classes = [api.permissions.IsSuperuser & api.permissions.IsVolunteer]
    serializer_class = api.serializers.user.PasswordValidatorSerializer

    @staticmethod
    def post(request):
        try:
            validate_password(request.data['password'])
            return Response({'can_use': True})
        except ValidationError:
            return Response({'can_use': False})
        except KeyError:
            return Response({'error': '"password"字段是必填项'}, status=400)


class UsersView(generics.ListAPIView):
    permission_classes = [api.permissions.IsSuperuser & api.permissions.IsVolunteer]
    pagination_class = api.pagination.LimitedLimitOffsetPagination
    serializer_class = api.serializers.user.UserSerializer

    def get_queryset(self):
        user_type = self.kwargs['user_type']
        try:
            user_type = {'student': 0, 'school': 1, 'volunteer': 2}[user_type]
        except KeyError:
            raise Http404
        return User.objects.filter(user_type=user_type)


class UsersChangePasswordView(generics.GenericAPIView):
    permission_classes = [api.permissions.IsSuperuser & api.permissions.IsVolunteer]
    serializer_class = api.serializers.user.ChangePasswordSerializer

    @staticmethod
    def patch(request):
        serializer = api.serializers.user.ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=204)
        else:
            return Response(serializer.errors, 400)


class UserView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [api.permissions.IsSuperuser & api.permissions.IsVolunteer]
    serializer_class = api.serializers.user.UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


class UserCreateView(generics.CreateAPIView):
    permission_classes = [api.permissions.IsSuperuser & api.permissions.IsVolunteer]
    serializer_class = api.serializers.user.UserCreateSerializer

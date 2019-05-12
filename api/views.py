from django.http import Http404, HttpResponse
from django.contrib import auth
from django.middleware import csrf
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import permissions, generics
from rest_framework.response import Response

import api.pagination
import api.permissions
import api.serializers
from account.models import User


def csrf_token_view(request):
    csrf.get_token(request)
    return HttpResponse(status=204)


class AccountSession(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = api.serializers.account.SessionSerializer

    @staticmethod
    def post(request):
        serializer = api.serializers.account.SessionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return HttpResponse(status=204)
        else:
            return Response(serializer.errors, 400)

    @staticmethod
    def delete(request):
        auth.logout(request)
        return HttpResponse(status=204)


class AccountInfo(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @staticmethod
    def get(request):
        user_info = {
            'is_logged_in': request.user.is_authenticated,
            'display_name': None,
            'gender': None,
            'user_type': None,
        }
        if user_info['is_logged_in']:
            user_info['display_name'] = request.user.display_name
            user_info['gender'] = request.user.gender
            user_info['user_type'] = request.user.user_type
            user_info['is_superuser'] = request.user.is_superuser
        return Response(user_info)


class AdminUsername(generics.GenericAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)

    @staticmethod
    def get(request):
        try:
            User.objects.get(username=request.query_params['u'])
            return Response({'can_use': False})
        except User.DoesNotExist:
            return Response({'can_use': True})
        except KeyError:
            return Response({'error': '"u"参数是必填项'}, status=400)


class AdminPassword(generics.GenericAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)

    @staticmethod
    def post(request):
        try:
            validate_password(request.data['password'])
            return Response({'can_use': True})
        except ValidationError:
            return Response({'can_use': False})
        except KeyError:
            return Response({'error': '"password"字段是必填项'}, status=400)


class AdminUsers(generics.ListAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    pagination_class = api.pagination.LimitedLimitOffsetPagination
    serializer_class = api.serializers.users.UserSerializer

    def get_queryset(self):
        user_type = self.kwargs['user_type']
        try:
            user_type = {'student': 0, 'school': 1, 'volunteer': 2}[user_type]
        except KeyError:
            raise Http404
        return User.objects.filter(user_type=user_type)


class AdminUsersPassword(generics.GenericAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)

    @staticmethod
    def patch(request):
        serializer = api.serializers.users.UsersPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=204)
        else:
            return Response(serializer.errors, 400)


class AdminUser(generics.UpdateAPIView, generics.DestroyAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    serializer_class = api.serializers.users.UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


class AdminUserCreate(generics.CreateAPIView):
    permissions = (api.permissions.IsSuperuser, api.permissions.IsVolunteer)
    serializer_class = api.serializers.users.UserPostSerializer

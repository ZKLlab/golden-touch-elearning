from django.http import HttpResponse
from django.contrib import auth
from rest_framework import permissions, generics
from rest_framework.response import Response

import api.pagination
import api.permissions
import api.serializers


class SessionView(generics.GenericAPIView):
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


class InfoView(generics.GenericAPIView):
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

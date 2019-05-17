from django.urls import path
from django.http import HttpResponse
from django.conf.urls import url
from django.middleware import csrf
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view

from . import views


def csrf_token_view(request):
    csrf.get_token(request)
    return HttpResponse(status=204)


app_name = 'api'
urlpatterns = [
    # Docs
    url(r'^docs$', get_swagger_view(title='API Docs')),
    # Basic
    path('csrf_token', csrf_token_view),
    # Account
    path('session', views.account.SessionView.as_view()),
    path('token', obtain_jwt_token),
    path('info', views.account.InfoView.as_view()),
    # User
    path('username', views.user.UsernameValidatorView.as_view()),
    path('password', views.user.PasswordValidatorView.as_view()),
    path('user', views.user.UserCreateView.as_view()),
    path('user/<int:id>', views.user.UserView.as_view()),
    path('users', views.user.UsersChangePasswordView.as_view()),
    path('users/<str:user_type>', views.user.UsersView.as_view()),
]

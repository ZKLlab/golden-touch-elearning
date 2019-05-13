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
    # Basic Views
    path('csrf_token', csrf_token_view),
    # Account
    path('session', views.account.SessionView.as_view()),
    path('token', obtain_jwt_token),
    path('info', views.account.InfoView.as_view()),
    # Admin
    path('username', views.users.UsernameValidatorView.as_view()),
    path('password', views.users.PasswordValidatorView.as_view()),
    path('user', views.users.UserCreateView.as_view()),
    path('user/<int:id>', views.users.UserView.as_view()),
    path('users', views.users.UsersChangePasswordView.as_view()),
    path('users/<str:user_type>', views.users.UsersView.as_view()),
]

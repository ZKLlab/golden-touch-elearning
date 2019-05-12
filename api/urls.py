from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

app_name = 'api'
urlpatterns = [
    path('csrf_token', views.csrf_token_view),
    # Account
    path('account/session', views.AccountSession.as_view()),
    path('account/token', obtain_jwt_token),
    path('account/info', views.AccountInfo.as_view()),
    # Admin
    path('admin/username', views.AdminUsername.as_view()),
    path('admin/password', views.AdminPassword.as_view()),
    path('admin/user', views.AdminUserCreate.as_view()),
    path('admin/user/<int:id>', views.AdminUser.as_view()),
    path('admin/users', views.AdminUsersPassword.as_view()),
    path('admin/users/<str:user_type>', views.AdminUsers.as_view()),
]

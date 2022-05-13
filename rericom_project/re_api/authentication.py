from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
import jwt
from decouple import config
from rest_framework.permissions import BasePermission


# class JWTAuth(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         token = request.META.get('HTTP_AUTHORIZATION')
#         print(token)
#         token_data = jwt.decode(token, config('SECRET_JWT'), algorithms=["HS256"])
#         print(token_data)
        # token_data.get('user_id')
        # try:
        #     user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     raise exceptions.AuthenticationFailed('No such user')
        #
        # return (user, None)


class PermissionCheck(BasePermission):
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION')
        token_data = jwt.decode(token, config('SECRET_JWT'), algorithms=["HS256"])
        flag = token_data.get('post_message_confirm', False)

        return flag



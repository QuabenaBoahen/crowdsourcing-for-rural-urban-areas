from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class CustomAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            valid_user = User.objects.get(username=username)
            valid_pwd = check_password(password, valid_user.password)
            if valid_user and valid_pwd:
                return valid_user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

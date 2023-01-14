from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from myapp.models import Profile


class login_backend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            o = Profile.objects.get(user_name=username, password=password)
        except Profile.DoesNotExist:
            return None
        return get_user_model().objects.get(user_name=o.user_name)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

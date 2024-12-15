from django.contrib.auth.backends import BaseBackend
from accounts.models import User


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = User
        try:
            user = user_model.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

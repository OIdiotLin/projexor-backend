from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from singleton_decorator import singleton


@singleton
class UserController:
    User = get_user_model()

    def create(self, **details):
        try:
            user = self.User.objects.create_user(**details)
            if user:
                return user
        except Exception as e:
            print(e)
        return None

    def get_list(self, **details):
        if details:
            users = self.User.objects.filter(**details)
        else:
            users = self.User.objects.all()
        return users

    def get_by_id(self, user_id):
        user = self.User.objects.get(id=user_id)
        print(user)
        # print(type(user))
        return user

    def update(self, **details):
        if details:
            user = self.User.objects.get_list(details['id'])
            user.update(**details)
            user.refresh_from_db()
            return user
        return None

    def delete(self, **details):
        if details:
            self.User.objects.filter(**details).delete()
            return True
        return False

    def login(self, username, password):
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            token = api_settings.JWT_ENCODE_HANDLER(api_settings.JWT_PAYLOAD_HANDLER(user))
            update_last_login(None, user)
            return user, token
        return None, None

from django.contrib.auth import get_user_model
from singleton_decorator import singleton


@singleton
class UserController:
    User = get_user_model()

    def create(self, **details):
        try:
            user = self.User.objects.create_user(**details)
            print(type(user))
            if user:
                return user
        except Exception as e:
            print(e)
        return None

    def get(self, **details):
        if details:
            users = self.User.objects.filter(**details)
        else:
            users = self.User.objects.all()
        return users

    def update(self, **details):
        if details:
            user = self.User.objects

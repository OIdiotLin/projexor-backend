from django.urls import path

from apis.views import user

urlpatterns = [
    path('users/', user.get_all, name='user-get-all'),
    path('users/register/', user.register, name='user-register')
]
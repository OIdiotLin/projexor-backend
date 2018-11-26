from django.urls import path

from apis.views import user, project

urlpatterns = [
    path('users/', user.get_all, name='user-get-all'),
    path('users/register/', user.register, name='user-register'),
    path('users/login/', user.login, name='user-login'),

    path('projects/', project.get_all, name='project-get-all')
]
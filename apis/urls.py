from django.urls import path

from apis.views import user, project

urlpatterns = [
    path('users/', user.get_list, name='user-get-list'),
    path('users/register/', user.register, name='user-register'),
    path('users/login/', user.login, name='user-login'),
    path('users/<id>/', user.get, name='user-get'),

    path('projects/', project.get_list, name='project-get-list')
]
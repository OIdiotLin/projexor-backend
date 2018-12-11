from django.urls import path

from apis.views import user, project, task

urlpatterns = [
    path('users/', user.get_list, name='user-get-list'),
    path('users/register/', user.register, name='user-register'),
    path('users/login/', user.login, name='user-login'),
    path('users/<id>/', user.get, name='user-get'),

    path('projects/', project.get_list_or_create, name='project-get-list-or-create'),
    path('projects/<id>/', project.single_entity, name='project-single'),

    path('tasks/', task.get_list_or_create, name='task-get-list-or-create'),
    path('tasks/<id>/', task.single_entity, name='task-single'),
]
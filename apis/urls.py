from django.urls import path

from apis.views import user, project, task, resource

urlpatterns = [
    path('users/', user.get_list, name='user-get-list'),
    path('users/register/', user.register, name='user-register'),
    path('users/login/', user.login, name='user-login'),
    path('users/<id>/', user.get, name='user-get'),

    path('projects/', project.get_list, name='project-get-list'),
    path('projects/<id>/', project.single_entity, name='project-single'),

    path('tasks/', task.get_list, name='task-get-list'),
    path('tasks/<id>/', task.single_entity, name='task-single'),

    path('resources/', resource.get_list_or_create, name='resource-get-list-or-create'),
    path('resources/<id>/', resource.single_entity, name='resource-single'),
]
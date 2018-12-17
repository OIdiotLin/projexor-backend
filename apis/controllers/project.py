
from django.db.models import F
from singleton_decorator import singleton

from apis.models import Project, UserInProject, User

@singleton
class ProjectController:
    def create(self, **details):
        users = details.pop('users')
        project = Project.objects.create(**details)
        self._update_users(project, set([user['id'] for user in users]))

        return project

    def delete(self, id):
        if id:
            Project.objects.get(id=id).delete()
            return True
        return False

    def update(self, **details):
        if details:
            project_id = details.pop('id')
            project = Project.objects.get(id=project_id)
            for attr, val in details.items():
                if attr == 'users':
                    updating_users = set([user['id'] for user in val])
                    self._update_users(project, updating_users)
                else:
                    setattr(project, attr, val)
            project.save()
            return True
        return False

    def _update_users(self, project_obj, users):
        existed_users = set([str(x) for x in project_obj.users.values_list('id', flat=True)])
        adding_users = users - existed_users
        removing_users = existed_users - users
        self._add_users(project_obj, adding_users)
        self._rmv_users(project_obj, removing_users)

    def _add_users(self, project_obj, users_id):
        rel = Project.users.through
        rel.objects.bulk_create([
            rel(project=project_obj, user=User.objects.get(id=user)) for user in users_id
        ])

    def _rmv_users(self, project_obj, users_id):
        rel = Project.users.through
        rel.objects.filter(project=project_obj.id, user__id__in=users_id).delete()

    def get_list(self, **details):
        projects = Project.objects.filter(**details)
        return projects

    def get_single(self, id):
        if id:
            project = Project.objects.get(id=id)
            return project
        return None


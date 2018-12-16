from singleton_decorator import singleton

from apis.models import Task, User


@singleton
class TaskController:
    def create(self, **details):
        users = details.pop('users')
        task = Task.objects.create(**details)
        self._update_users(task, set([user['id'] for user in users]))
        return task

    def delete(self, id):
        if id:
            Task.objects.get(id=id).delete()
            return True
        return False

    def update(self, **details):
        if details:
            task_id = details.pop('id')
            task = Task.objects.get(id=task_id)
            for attr, val in details.items():
                if attr == 'project':
                    pass
                elif attr == 'users':
                    updating_users = set([user['id'] for user in val])
                    self._update_users(task, updating_users)
                else:
                    setattr(task, attr, val)
            task.save()
            return True
        return False
    
    def _update_users(self, task_obj, users):
        existed_users = set([str(x) for x in task_obj.users.values_list('id', flat=True)])
        adding_users = users - existed_users
        removing_users = existed_users - users
        self._add_users(task_obj, adding_users)
        self._rmv_users(task_obj, removing_users)

    def _add_users(self, task_obj, users_id):
        rel = Task.users.through
        rel.objects.bulk_create([
            rel(task=task_obj, user=User.objects.get(id=user)) for user in users_id
        ])

    def _rmv_users(self, task_obj, users_id):
        rel = Task.users.through
        rel.objects.filter(task=task_obj.id, user__id__in=users_id).delete()

    def get_list(self, **details):
        tasks = Task.objects.filter(**details)
        return tasks

    def get_single(self, id):
        if id:
            task = Task.objects.get(id=id)
            return task
        return None

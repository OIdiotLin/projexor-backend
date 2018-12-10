from singleton_decorator import singleton

from apis.models import Task


@singleton
class TaskController:
    def create(self, **details):
        task = Task.objects.create(**details)
        return task

    def delete(self, id):
        if id:
            Task.objects.get(id=id).delete()
            return True
        return False

    def update(self, **details):
        if details:
            id = details.pop('id')
            Task.objects.filter(id=id).update(**details)
            return True
        return False

    def get_list(self, **details):
        tasks = Task.objects.filter(**details)
        return tasks

    def get_single(self, id):
        if id:
            task = Task.objects.get(id=id)
            return task
        return None

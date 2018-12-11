from singleton_decorator import singleton

from apis.models import Project


@singleton
class ProjectController:
    def create(self, **details):
        project = Project.objects.create(**details)
        return project

    def delete(self, id):
        if id:
            Project.objects.get(id=id).delete()
            return True
        return False

    def update(self, **details):
        if details:
            id = details.pop('id')
            Project.objects.filter(id=id).update(**details)
            return True
        return False

    def get_list(self, **details):
        projects = Project.objects.filter(**details)
        return projects

    def get_single(self, id):
        if id:
            project = Project.objects.get(id=id)
            return project
        return None




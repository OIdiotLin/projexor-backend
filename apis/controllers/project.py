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
        # TODO 编写 update 结果
        if details:
            project = Project.objects.get(id=details['id'])
            print(project)
        return True

    def get_list(self, **details):
            # print(details)
        projects = Project.objects.filter(**details)
        return projects

    def get_single(self, id):
        if id:
            project = Project.objects.get(id=id)
            return project
        return None




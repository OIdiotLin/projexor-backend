from singleton_decorator import singleton

from apis.models import Resource


@singleton
class ResourceController:
    def create(self, **details):
        resource = Resource.objects.create(**details)
        return resource

    def delete(self, id):
        if id:
            Resource.objects.get(id=id).delete()
            return True
        return False

    def update(self, **details):
        if details:
            resource_id = details.pop('id')
            resource = Resource.objects.get(id=resource_id)
            for attr, val in details.items():
                if attr == 'project':
                    pass
                else:
                    setattr(resource, attr, val)
            resource.save()
            return True
        return False

    def get_list(self, **details):
        resources = Resource.objects.filter(**details)
        return resources

    def get_single(self, id):
        if id:
            resource = Resource.objects.get(id=id)
            return resource
        return None

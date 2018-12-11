from singleton_decorator import singleton

from apis.models import Reply


@singleton
class ReplyController:
    def create(self, **details):
        reply = Reply.objects.create(**details)
        return reply

    def delete(self, id):
        if id:
            Reply.objects.get(id=id).delete()
            return True
        return False

    def update(self, **details):
        if details:
            id = details.pop('id')
            Reply.objects.filter(id=id).update(**details)
            return True
        return False

    def get_list(self, **details):
        replys = Reply.objects.filter(**details)
        return replys

    def get_single(self, id):
        if id:
            reply = Reply.objects.get(id=id)
            return reply
        return None

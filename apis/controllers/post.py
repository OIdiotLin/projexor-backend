from singleton_decorator import singleton

from apis.models import Post


@singleton
class PostController:
    def create(self, **details):
        post = Post.objects.create(**details)
        return post

    def delete(self, id):
        if id:
            Post.objects.get(id=id).delete()
            return True
        return False

    def update(self, **details):
        if details:
            post_id = details.pop('id')
            post = Post.objects.get(id=post_id)
            for attr, val in details.items():
                if attr == 'project':
                    pass
                elif attr == 'user':
                    pass
                else:
                    setattr(post, attr, val)
            post.save()
            return True
        return False

    def get_list(self, **details):
        posts = Post.objects.filter(**details)
        return posts

    def get_single(self, id):
        if id:
            post = Post.objects.get(id=id)
            return post
        return None

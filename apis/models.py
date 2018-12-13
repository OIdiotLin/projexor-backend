import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.utils.datetime_safe import datetime

"""
提醒大家的话：

1. 建立多对多关系时，使用手动编写中间表的方法，并在关联表中使用 `through` 显式地制定中间表名。
   可见 User，Project 与 UserInProject 的例子。
2. 在 serializers.py 中建立相应的（反）序列化类。

"""


class User(AbstractUser):
    """用户表
    https://www.jianshu.com/p/b993f4feff83
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Project(models.Model):
    """项目表
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='空项目', null=False)
    users = models.ManyToManyField(get_user_model(), through='UserInProject')

    def __str__(self):
        return '{name} {id}'.format(name=str(self.name), id=str(self.id)[:8])

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


class UserInProject(models.Model):
    """用户 - 项目 多对多关系表

    Fields:
        id: 关系 id
        user: 关联用户 User 的 id
        project: 关联项目 Project 的 id
        owner: 是否是项目发起人
        admin: 是否有项目内容管理权限
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.BooleanField(default=False, null=False)
    admin = models.BooleanField(default=False, null=False)

    def __str__(self):
        return '{username} @ {project}'.format(username=str(self.user.username), project=str(self.project))

    class Meta:
        verbose_name = '用户 - 项目关系'
        verbose_name_plural = '用户 - 项目关系'


class Resource(models.Model):
    """资源表

    Fields:
        id: 资源 id
        name: 资源名称
        description: 描述
        total: 总量
        remainder: 余量（如果为可消耗品则为 null）
        unit: 单位
        project: 关联项目 Project 的 id
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='新资源', null=False)
    description = models.TextField(max_length=512, blank=True)
    total = models.FloatField()
    remainder = models.FloatField(null=True)
    unit = models.CharField(max_length=20, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return '{name} @ {project}'.format(name=str(self.name), project=str(self.project))

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = '资源'


class Task(models.Model):
    """任务表

    Fields:
        id: 任务 id
        name: 任务名称
        description: 描述
        begin_time: 开始时间
        end_time: 结束时间
        state: 状态 (正在进行 running, 已经结束 finished)
        project: 关联项目 Project 的 id
        users: 关联用户 User 的 id
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='新任务', null=False)
    description = models.TextField(max_length=512, blank=True)
    begin_time = models.DateTimeField(default=datetime.now, null=False)
    end_time = models.DateTimeField(default=datetime.now, null=False)
    state = models.CharField(max_length=10,
                             choices=(('R', 'running'), ('F', 'finished')),
                             default='R')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    users = models.ManyToManyField(get_user_model(), through='UserInTask')

    def __str__(self):
        return '{name} @ {project}'.format(name=str(self.name), project=str(self.project))

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务'


class UserInTask(models.Model):
    """用户 - 任务 多对多关系表

    Fields:
        id: 关系 id
        user: 关联用户 User 的 id
        task: 关联任务 Task 的 id
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return '{name} @ {project}'.format(name=str(self.user.username), project=str(self.task.name))

    class Meta:
        verbose_name = '用户 - 任务关系'
        verbose_name_plural = '用户 - 任务关系'


class Post(models.Model):
    """讨论帖表

    Fields:
        id: 讨论帖 id
        title: 标题
        content: 内容
        time: 创建时间
        project: 关联项目 Project 的 id
        user: 关联用户 User 的 id
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, default='新讨论帖', null=False)
    content = models.TextField(max_length=2048, default='讨论内容', null=False)
    time = models.DateTimeField(default=datetime.now, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return '{title} @ {project}'.format(title=str(self.title), project=str(self.project))

    class Meta:
        verbose_name = '讨论帖'
        verbose_name_plural = '讨论帖'


class Reply(models.Model):
    """讨论回复表

    Fields:
        id: 回复 id
        content: 内容
        time: 创建时间
        post: 关联讨论帖 Post 的 id
        user: 关联用户 User 的 id
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=2048, default='讨论内容', null=False)
    time = models.DateTimeField(default=datetime.now, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return '{content}... @ {post}...'.format(content=self.content[:6], post=self.post.title[:6])

    class Meta:
        verbose_name = '讨论回复'
        verbose_name_plural = '讨论回复'


def project_storage_path(instance, filename):
    """https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.FileField.upload_to"""
    return '{project}/{filename}'.format(project=str(instance.project), filename=filename)


class File(models.Model):
    """上传文件列表

    Fields:
        id: 文件 id
        file: 文件 url
        time: 上传时间
        project: 关联项目 project 的 id
        user: 关联用户 user 的 id
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, default='新文件')
    file = models.FileField(upload_to=project_storage_path)
    time = models.DateTimeField(default=datetime.now, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file.name)

    class Meta:
        verbose_name = '文件'
        verbose_name_plural = '文件'

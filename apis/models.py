import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

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


class Project(models.Model):
    """项目表
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='空项目', null=False)
    users = models.ManyToManyField(get_user_model(), through='UserInProject')


class UserInProject(models.Model):
    """用户 - 项目 多对多关系表

    Fields:
        id: 关系 id
        user_id: 关联用户 User 的 id
        project_id: 关联项目 Project 的 id
        owner: 是否是项目发起人
        admin: 是否有项目内容管理权限
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.BooleanField(default=False, null=False)
    admin = models.BooleanField(default=False, null=False)


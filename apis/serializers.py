from django.contrib.auth import get_user_model
from rest_framework import serializers

from apis.models import Project, Resource, Task, Post, Reply

"""
序列化类

参见 https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'date_joined', 'last_login', 'is_superuser')


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Resource
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    users = UserSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    user = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    post = PostSerializer()
    user = UserSerializer()

    class Meta:
        model = Reply
        fields = '__all__'

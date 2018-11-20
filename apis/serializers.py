from django.contrib.auth import get_user_model
from rest_framework import serializers

from apis.models import Project


"""
序列化类

参见 https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'date_joined', 'last_login', 'is_superuser')

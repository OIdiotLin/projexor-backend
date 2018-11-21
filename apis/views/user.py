from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from apis.serializers import UserSerializer


@api_view(['POST'])
def register(request):
    """注册新用户
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all(request):
    """查询用户
    """
    users = get_user_model().objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    """用户登录

    登录系统，并获取 token
    """
    username = request.data.get('username')
    password = request.data.get('password')
    # 登录
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        token = api_settings.JWT_ENCODE_HANDLER(api_settings.JWT_PAYLOAD_HANDLER(user))
        update_last_login(None, user)
        serializer = UserSerializer(user)
        return Response(data={
            'token': token,
            'user': serializer.data
        }, headers={
            'Set-Cookie': 'token={}'.format(token)  # 提供 Cookies
        })

    return Response("hahaha", status=status.HTTP_401_UNAUTHORIZED)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apis.controllers.user import UserController
from apis.serializers import UserSerializer


@api_view(['POST'])
def register(request):
    """注册新用户
    """
    details = dict(request.data)
    user = UserController().create(**details)
    if user:
        serializer = UserSerializer(data=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_list(request):
    """查询用户列表
    """
    details = request.GET.dict()
    users = UserController().get_list(**details)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get(request, id):
    """通过 id 查询某个用户
    """
    user = UserController().get_by_id(id)
    if user:
        serializer = UserSerializer(user)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login(request):
    """用户登录

    登录系统，并获取 token
    """
    username = request.data.get('username')
    password = request.data.get('password')
    # 登录
    user, token = UserController().login(username, password)
    if user:
        serializer = UserSerializer(user)
        return Response(data={
            'token': token,
            'user': serializer.data
        }, headers={
            'Set-Cookie': 'token={}'.format(token)  # 提供 Cookies
        })

    return Response(None, status=status.HTTP_401_UNAUTHORIZED)

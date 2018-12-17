from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apis.controllers.post import PostController
from apis.serializers import PostSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def get_list_or_create(request):
    """查询帖子列表 or 新建一个帖子
    """
    if request.method == 'GET':
        details = request.GET.dict()
        posts = PostController().get_list(**details)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        details = dict(request.data)
        post = PostController().create(**details)
        if post:
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', 'DELETE', 'GET'])
@permission_classes((IsAuthenticated,))
def single_entity(request, id):
    """通过 id 访问某个帖子，进行查询、修改、删除等操作
    """
    if request.method == 'GET':
        post = PostController().get_single(id=id)
        if post:
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        res = PostController().delete(id=id)
        if res:
            return Response(None, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        details = dict(request.data)
        res = PostController().update(**details)
        if res:
            post = PostController().get_single(id=id)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        details = dict(request.data)
        res = PostController().update(**details)
        if res:
            post = PostController().get_single(id=id)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

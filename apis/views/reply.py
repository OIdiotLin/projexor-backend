from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apis.controllers.reply import ReplyController
from apis.serializers import ReplySerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def get_list_or_create(request):
    """查询回复列表 or 新建一个回复
    """
    if request.method == 'GET':
        details = request.GET.dict()
        replies = ReplyController().get_list(**details)
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        details = dict(request.data)
        reply = ReplyController().create(**details)
        if reply:
            serializer = ReplySerializer(reply)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', 'DELETE', 'GET'])
@permission_classes((IsAuthenticated,))
def single_entity(request, id):
    """通过 id 访问某个回复，进行查询、修改、删除等操作
    """
    if request.method == 'GET':
        reply = ReplyController().get_single(id=id)
        if reply:
            serializer = ReplySerializer(reply)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        res = ReplyController().delete(id=id)
        if res:
            return Response(None, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        details = dict(request.data)
        res = ReplyController().update(**details)
        if res:
            reply = ReplyController().get_single(id=id)
            serializer = ReplySerializer(reply)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        details = dict(request.data)
        res = ReplyController().update(**details)
        if res:
            reply = ReplyController().get_single(id=id)
            serializer = ReplySerializer(reply)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

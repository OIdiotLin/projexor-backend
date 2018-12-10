import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apis.controllers.task import TaskController
from apis.serializers import TaskSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_list(request):
    """查询任务列表
    """
    details = request.GET.dict()
    tasks = TaskController().get_list(**details)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create(request):
    """新建一个任务
    """
    details = dict(request.data)
    task = TaskController().create(**details)
    if task:
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', 'DELETE', 'GET'])
@permission_classes((IsAuthenticated,))
def single_entity(request, id):
    """通过 id 访问某个任务，进行查询、修改、删除等操作
    """
    if request.method == 'GET':
        task = TaskController().get_single(id=id)
        if task:
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        res = TaskController().delete(id=id)
        if res:
            return Response(None, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        details = json.loads(request.body)
        res = TaskController().update(**details)
        if res:
            task = TaskController().get_single(id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        details = json.loads(request.body)
        res = TaskController().update(**details)
        if res:
            task = TaskController().get_single(id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

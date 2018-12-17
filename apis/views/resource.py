import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apis.controllers.resource import ResourceController
from apis.serializers import ResourceSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def get_list_or_create(request):
    """查询资源列表 or 新建一个资源
    """
    if request.method == 'GET':
        details = request.GET.dict()
        resources = ResourceController().get_list(**details)
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        details = dict(request.data)
        resource = ResourceController().create(**details)
        if resource:
            serializer = ResourceSerializer(resource)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', 'DELETE', 'GET'])
@permission_classes((IsAuthenticated,))
def single_entity(request, id):
    """通过 id 访问某个资源，进行查询、修改、删除等操作
    """
    if request.method == 'GET':
        resource = ResourceController().get_single(id=id)
        if resource:
            serializer = ResourceSerializer(resource)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        res = ResourceController().delete(id=id)
        if res:
            return Response(None, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        details = dict(request.data)
        res = ResourceController().update(**details)
        if res:
            resource = ResourceController().get_single(id=id)
            serializer = ResourceSerializer(resource)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        details = dict(request.data)
        res = ResourceController().update(**details)
        if res:
            resource = ResourceController().get_single(id=id)
            serializer = ResourceSerializer(resource)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

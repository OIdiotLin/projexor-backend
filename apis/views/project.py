from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apis.controllers.project import ProjectController
from apis.serializers import ProjectSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def get_list_or_create(request):
    """查询项目列表 or 新建一个项目
    """
    if request.method == 'GET':
        details = request.GET.dict()
        projects = ProjectController().get_list(**details)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        details = dict(request.data)
        project = ProjectController().create(**details)
        if project:
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', 'DELETE', 'GET'])
@permission_classes((IsAuthenticated, ))
def single_entity(request, id):
    """通过 id 访问某个项目，进行查询、修改、删除等操作
    """
    if request.method == 'GET':
        project = ProjectController().get_single(id=id)
        if project:
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        res = ProjectController().delete(id=id)
        if res:
            return Response(None, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        details = dict(request.data)
        res = ProjectController().update(**details)
        if res:
            project = ProjectController().get_single(id=id)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        details = dict(request.data)
        res = ProjectController().update(**details)
        if res:
            project = ProjectController().get_single(id=id)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

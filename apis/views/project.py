from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apis.models import Project
from apis.serializers import ProjectSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_all(request):
    """查询所有项目
    """
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)

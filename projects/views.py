from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from projects.models import *
from projects.serializers import *


class ProjectsViewset(ListModelMixin, GenericViewSet):
    serializer_class = ProjectSerializer
    queryset = Project

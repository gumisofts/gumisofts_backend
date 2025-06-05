from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import *


class MessageViewset(CreateModelMixin, GenericViewSet):
    serializer_class = MessageSerializer


class MissionViewset(ListModelMixin, GenericViewSet):
    serializer_class = MissionSerializer
    queryset = Mission.objects.all()

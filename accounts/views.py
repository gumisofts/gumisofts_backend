from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import *


class MessageViewset(CreateModelMixin, GenericViewSet):
    serializer_class = MessageSerializer

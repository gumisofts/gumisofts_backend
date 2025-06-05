from rest_framework.serializers import Serializer, ModelSerializer
from .models import *


class MessageSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Message


class MissionSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Mission

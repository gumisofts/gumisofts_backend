from rest_framework.serializers import ModelSerializer, Serializer

from .models import *


class MessageSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Message


class MissionSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Mission

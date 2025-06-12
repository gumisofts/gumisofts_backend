from rest_framework.serializers import ModelSerializer, Serializer

from .models import *


class MessageSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Message
        read_only_fields = ["is_read"]

from rest_framework.serializers import ModelSerializer, Serializer

from .models import *


class ProjectSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Project

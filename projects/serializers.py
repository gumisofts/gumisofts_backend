from rest_framework.serializers import Serializer, ModelSerializer
from .models import *


class ProjectSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Project

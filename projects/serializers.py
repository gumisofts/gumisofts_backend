from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from .models import *


class ProjectSerializer(ModelSerializer):
    technologies = serializers.SerializerMethodField()

    def get_technologies(self, obj):
        return [tech["name"] for tech in obj.technologies.all().values("name")]

    class Meta:
        exclude = []
        model = Project

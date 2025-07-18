from rest_framework.serializers import ModelSerializer, Serializer

from .models import *


class MessageSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Message
        read_only_fields = ["is_read"]


class CompanyStatsSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = CompanyStats
        read_only_fields = []


class OrganizationSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Organization
        read_only_fields = []

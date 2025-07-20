from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import *


class TestimonalSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Testimonal


class ServiceSerializer(ModelSerializer):
    features = serializers.StringRelatedField(many=True)

    class Meta:
        exclude = []
        model = Service

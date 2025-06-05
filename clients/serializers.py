from rest_framework.serializers import ModelSerializer
from .models import *


class TestimonalSerializer(ModelSerializer):
    class Meta:
        exclude = []
        model = Testimonal

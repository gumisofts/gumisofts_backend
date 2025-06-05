from django.shortcuts import render
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Client
from .serializers import *


class ClientCount(APIView):
    def get(self, request):
        client_count = Client.objects.filter()
        return {"client_count": client_count}


class TestimonalViewset(ListModelMixin, GenericViewSet):
    serializer_class = TestimonalSerializer
    queryset = Testimonal.objects.all()

from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import *


class MessageViewset(CreateModelMixin, GenericViewSet):
    serializer_class = MessageSerializer


class CompanyStatsViewset(ListModelMixin, GenericViewSet):
    serializer_class = CompanyStatsSerializer
    queryset = CompanyStats.objects.all()


class OrganizationViewset(GenericViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.filter(is_default=True)

    @action(detail=False, methods=["get"])
    def default(self, request):
        organization = self.queryset.first()
        serializer = self.get_serializer(organization)
        return Response(serializer.data)

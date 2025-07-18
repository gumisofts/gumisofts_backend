from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Job, JobApplication
from .serializers import JobApplicationSerializer, JobSerializer


class JobViewset(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = Job.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        serializer_class=JobApplicationSerializer,
    )
    def apply(self, request, pk=None):

        job = self.get_object()

        serializer = self.get_serializer(data=request.data, context={"job": job})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = JobApplication.objects.all()
        job_id = self.request.query_params.get("job_id", None)
        if job_id:
            queryset = queryset.filter(job_id=job_id)
        return queryset


# class ApplicationViewSet(viewsets.ModelViewSet):
#     queryset = JobApplication.objects.all()
#     serializer_class = JobApplicationSerializer
#     permission_classes = [permissions.IsAdminUser]

#     def get_queryset(self):
#         queryset = JobApplication.objects.all()
#         job_id = self.request.query_params.get("job_id", None)
#         if job_id:
#             queryset = queryset.filter(job_id=job_id)
#         return queryset

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["request"] = self.request
#         return context

#     @action(detail=True, methods=["post"])
#     def update_status(self, request, pk=None):
#         application = self.get_object()
#         new_status = request.data.get("status")
#         if new_status in dict(JobApplication._meta.get_field("status").choices):
#             application.status = new_status
#             application.save()
#             return Response({"message": "Status updated successfully"})
#         return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

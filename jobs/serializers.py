import os

from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from .models import Job, JobApplication, Salary


class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = ["min", "max", "currency"]


class JobSerializer(serializers.ModelSerializer):
    benefits = serializers.StringRelatedField(many=True)
    requirements = serializers.StringRelatedField(many=True)
    responsibilities = serializers.StringRelatedField(many=True)
    salary = SalarySerializer(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ("posted_at",)


class CurrentJobDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["job"]

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class JobApplicationSerializer(serializers.ModelSerializer):
    job = serializers.HiddenField(default=CurrentJobDefault())

    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ("applied_date", "status")
        extra_kwargs = {
            "resume": {
                "validators": [
                    FileExtensionValidator(
                        allowed_extensions=["pdf", "doc", "docx", "txt"]
                    )
                ]
            }
        }

        def validate_resume(self, value):
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    {"resume": "Resume file size must be less than 5MB."}
                )
            if not value.name.endswith((".pdf", ".doc", ".docx", ".txt")):
                raise serializers.ValidationError(
                    {"resume": "Resume must be a PDF, DOC, DOCX, or TXT file."}
                )
            return value

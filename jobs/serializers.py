from rest_framework import serializers
from .models import Job, JobApplication
from django.core.validators import FileExtensionValidator
import os

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('posted_date',)

class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    resume_url = serializers.SerializerMethodField()
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('applied_date', 'status')

    def get_resume_url(self, obj):
        if obj.resume:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resume.url)
            return obj.resume.url
        return None

    def validate_resume(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx']
        if ext.lower() not in valid_extensions:
            raise serializers.ValidationError('Only PDF and Word documents are allowed.')
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError('File size cannot exceed 5MB.')
        return value

    def validate(self, data):
        job = data.get('job')
        if not job.is_active:
            raise serializers.ValidationError('This job posting is no longer active.')
        return data
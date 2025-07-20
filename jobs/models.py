import os

from django.db import models
from rest_framework import permissions, viewsets
from rest_framework.decorators import action


class JobRequirement(models.Model):
    requirement = models.CharField(max_length=255)

    def __str__(self):
        return self.requirement


class JobBenefit(models.Model):
    benefit = models.CharField(max_length=255)

    def __str__(self):
        return self.benefit


class JobResponsibility(models.Model):
    responsibility = models.CharField(max_length=255)

    def __str__(self):
        return self.responsibility


class Salary(models.Model):
    min = models.IntegerField()
    max = models.IntegerField()
    currency = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.min} - {self.max} {self.currency}"


class Job(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    EMPLOYMENT_TYPES = [
        ("full-time", "Full Time"),
        ("part-time", "Part Time"),
        ("contract", "Contract"),
        ("internship", "Internship"),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default="Engineering")
    description = models.TextField()
    type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES)
    salary = models.ForeignKey(
        Salary, on_delete=models.CASCADE, related_name="jobs", null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=255, default="Remote")
    experience = models.CharField(max_length=255, default="2+")
    requirements = models.ManyToManyField(JobRequirement)
    responsibilities = models.ManyToManyField(JobResponsibility)
    benefits = models.ManyToManyField(JobBenefit)

    deadline = models.DateTimeField(null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-posted_at"]


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=[
            ("pending", "Pending"),
            ("reviewed", "Reviewed"),
            ("shortlisted", "Shortlisted"),
            ("rejected", "Rejected"),
            ("interview", "Interview Scheduled"),
            ("offer", "Job Offer Extended"),
        ],
    )

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the original status to detect changes
        self._original_status = self.status

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the original status after saving
        self._original_status = self.status

    class Meta:
        ordering = ["-applied_date"]


# {
#         id: '1',
#         title: 'Senior Full-Stack Developer',
#         department: 'Engineering',
#         location: 'Remote',
#         type: 'full-time',
#         experience: '5+ years',
#         description: 'We are looking for a passionate Senior Full-Stack Developer to join our growing team and help build innovative software solutions.',
#         requirements: [
#             '5+ years of experience in full-stack development',
#             'Proficiency in React, Node.js, and TypeScript',
#             'Experience with cloud platforms (AWS, GCP, or Azure)',
#             'Strong understanding of database design and optimization',
#             'Experience with microservices architecture'
#         ],
#         responsibilities: [
#             'Design and develop scalable web applications',
#             'Collaborate with cross-functional teams',
#             'Mentor junior developers',
#             'Participate in code reviews and technical discussions',
#             'Contribute to technical decision-making'
#         ],
#         benefits: [
#             'Competitive salary and equity',
#             'Flexible working hours',
#             'Health and dental insurance',
#             'Professional development budget',
#             'Latest tech equipment'
#         ],
#         salary: {
#             min: 80000,
#             max: 120000,
#             currency: 'USD'
#         },
#         postedAt: '2024-01-15',
#         deadline: '2024-02-15',
#         isActive: true
#     },

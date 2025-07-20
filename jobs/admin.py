from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    Job,
    JobApplication,
    JobBenefit,
    JobRequirement,
    JobResponsibility,
    Salary,
)
from .signals import send_interview_scheduled_email, send_offer_email


class InterviewScheduleForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    duration = forms.CharField(max_length=50, initial="1 hour")
    type = forms.ChoiceField(
        choices=[
            ("virtual", "Virtual/Video Call"),
            ("in-person", "In-Person"),
            ("phone", "Phone Call"),
        ]
    )
    location = forms.CharField(
        max_length=200, help_text="Meeting link for virtual, address for in-person"
    )
    interviewer = forms.CharField(max_length=200, initial="Hiring Team")
    personal_message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
        help_text="Optional personal message to include",
    )


class JobOfferForm(forms.Form):
    offer_link = forms.URLField(
        required=False, help_text="Link to detailed offer document"
    )
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), help_text="Response deadline"
    )
    personal_message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
        help_text="Personal message from the team",
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "location",
        "type",
        "is_active",
        "posted_at",
        "applications_count",
    )
    search_fields = ("title", "category", "location")
    list_filter = ("type", "category", "is_active", "posted_at")
    readonly_fields = ("posted_at",)

    def applications_count(self, obj):
        count = obj.applications.count()
        if count > 0:
            url = (
                reverse("admin:jobs_jobapplication_changelist")
                + f"?job__id__exact={obj.id}"
            )
            return format_html('<a href="{}">{} applications</a>', url, count)
        return "0 applications"

    applications_count.short_description = "Applications"


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "job_title",
        "email",
        "status_badge",
        "applied_date",
        "resume_link",
        "linkedin_link",
    )
    search_fields = ("full_name", "email", "job__title")
    list_filter = ("status", "applied_date", "job__category", "job__type")
    readonly_fields = ("applied_date", "resume_preview", "cover_letter_preview")

    fieldsets = (
        (
            "Application Details",
            {"fields": ("job", "full_name", "email", "linkedin", "applied_date")},
        ),
        (
            "Documents",
            {
                "fields": (
                    "resume",
                    "resume_preview",
                    "cover_letter",
                    "cover_letter_preview",
                )
            },
        ),
        ("Status", {"fields": ("status",)}),
    )

    def job_title(self, obj):
        return obj.job.title

    job_title.short_description = "Position"

    def status_badge(self, obj):
        colors = {
            "pending": "#fbbf24",
            "reviewed": "#f59e0b",
            "shortlisted": "#10b981",
            "interview": "#8b5cf6",
            "rejected": "#ef4444",
            "offer": "#06b6d4",
        }
        color = colors.get(obj.status, "#6b7280")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    def resume_link(self, obj):
        if obj.resume:
            return format_html(
                '<a href="{}" target="_blank">📄 View</a>', obj.resume.url
            )
        return "❌ None"

    resume_link.short_description = "Resume"

    def linkedin_link(self, obj):
        if obj.linkedin:
            return format_html(
                '<a href="{}" target="_blank">💼 LinkedIn</a>', obj.linkedin
            )
        return "❌ None"

    linkedin_link.short_description = "LinkedIn"

    def resume_preview(self, obj):
        if obj.resume:
            return format_html(
                '<a href="{}" target="_blank">📄 Download Resume</a><br>'
                "<small>File: {}</small>",
                obj.resume.url,
                obj.resume.name,
            )
        return "No resume uploaded"

    resume_preview.short_description = "Resume File"

    def cover_letter_preview(self, obj):
        if obj.cover_letter:
            return format_html(
                '<div style="max-height: 100px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; background: #f9f9f9;">{}</div>',
                obj.cover_letter[:500] + ("..." if len(obj.cover_letter) > 500 else ""),
            )
        return "No cover letter provided"

    cover_letter_preview.short_description = "Cover Letter"

    # Custom Admin Actions
    @admin.action(description="✅ Mark as Shortlisted")
    def mark_as_shortlisted(self, request, queryset):
        updated = queryset.update(status="shortlisted")
        self.message_user(
            request, f"Successfully shortlisted {updated} application(s)."
        )

    @admin.action(description="👀 Mark as Under Review")
    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(status="reviewed")
        self.message_user(
            request, f"Successfully marked {updated} application(s) as under review."
        )

    @admin.action(description="❌ Mark as Rejected")
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status="rejected")
        self.message_user(request, f"Successfully rejected {updated} application(s).")

    @admin.action(description="📅 Schedule Interview")
    def schedule_interview(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Please select exactly one application to schedule an interview.",
                level="ERROR",
            )
            return

        application = queryset.first()

        if request.method == "POST":
            form = InterviewScheduleForm(request.POST)
            if form.is_valid():
                interview_details = {
                    "date": form.cleaned_data["date"].strftime("%B %d, %Y"),
                    "time": form.cleaned_data["time"].strftime("%I:%M %p"),
                    "duration": form.cleaned_data["duration"],
                    "type": form.cleaned_data["type"],
                    "location": form.cleaned_data["location"],
                    "interviewer": form.cleaned_data["interviewer"],
                    "meeting_link": (
                        form.cleaned_data["location"]
                        if form.cleaned_data["type"] == "virtual"
                        else None
                    ),
                }

                # Update status and send email
                application.status = "interview"
                application.save()

                success = send_interview_scheduled_email(application, interview_details)
                if success:
                    self.message_user(
                        request,
                        f"Interview scheduled for {application.full_name}. Email sent successfully.",
                    )
                else:
                    self.message_user(
                        request,
                        f"Interview scheduled for {application.full_name}, but email failed to send.",
                        level="WARNING",
                    )

                return HttpResponseRedirect(request.get_full_path())
        else:
            form = InterviewScheduleForm()

        context = {
            "form": form,
            "application": application,
            "title": f"Schedule Interview - {application.full_name}",
        }
        return render(request, "admin/jobs/schedule_interview.html", context)

    @admin.action(description="🎉 Extend Job Offer")
    def extend_job_offer(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Please select exactly one application to extend a job offer.",
                level="ERROR",
            )
            return

        application = queryset.first()

        if request.method == "POST":
            form = JobOfferForm(request.POST)
            if form.is_valid():
                offer_details = {
                    "offer_link": form.cleaned_data["offer_link"],
                    "deadline": form.cleaned_data["deadline"].strftime("%B %d, %Y"),
                    "message": form.cleaned_data["personal_message"],
                }

                # Update status and send email
                application.status = "offer"
                application.save()

                success = send_offer_email(application, offer_details)
                if success:
                    self.message_user(
                        request,
                        f"Job offer extended to {application.full_name}. Email sent successfully.",
                    )
                else:
                    self.message_user(
                        request,
                        f"Job offer extended to {application.full_name}, but email failed to send.",
                        level="WARNING",
                    )

                return HttpResponseRedirect(request.get_full_path())
        else:
            form = JobOfferForm()

        context = {
            "form": form,
            "application": application,
            "title": f"Extend Job Offer - {application.full_name}",
        }
        return render(request, "admin/jobs/extend_offer.html", context)

    actions = [
        mark_as_shortlisted,
        mark_as_reviewed,
        mark_as_rejected,
        schedule_interview,
        extend_job_offer,
    ]


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ("salary_range", "currency")
    search_fields = ("currency",)

    def salary_range(self, obj):
        return f"{obj.min:,} - {obj.max:,}"

    salary_range.short_description = "Salary Range"


@admin.register(JobRequirement)
class JobRequirementAdmin(admin.ModelAdmin):
    list_display = ("requirement",)
    search_fields = ("requirement",)


@admin.register(JobResponsibility)
class JobResponsibilityAdmin(admin.ModelAdmin):
    list_display = ("responsibility",)
    search_fields = ("responsibility",)


@admin.register(JobBenefit)
class JobBenefitAdmin(admin.ModelAdmin):
    list_display = ("benefit",)
    search_fields = ("benefit",)

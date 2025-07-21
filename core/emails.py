from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils import timezone


def send_email_to_admins(subject: str, message: str, html_message: str = None):
    """Send email to admins with optional HTML content"""
    to_emails = list(map(lambda x: x[1], settings.ADMINS))
    return send_email_to(
        subject=subject, message=message, to_emails=to_emails, html_message=html_message
    )


def send_email_to(
    subject: str, message: str, to_emails: list, html_message: str = None
):
    """Send email with optional HTML content"""
    if html_message:
        # Send HTML email
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to_emails,
        )
        email.attach_alternative(html_message, "text/html")
        return email.send(fail_silently=False)
    else:
        # Send plain text email
        return send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            to_emails,
            fail_silently=False,
        )


def send_newsletter_subscription_confirmation(subscriber_email: str):
    """Send confirmation email to new newsletter subscriber"""
    from blog.models import NewsletterSubscriber

    # Get the subscriber instance to access unsubscribe token
    try:
        subscriber = NewsletterSubscriber.objects.get(email=subscriber_email)
        unsubscribe_url = f"https://gumisofts.com/newsletter/unsubscribe/{subscriber.unsubscribe_token}/"
    except NewsletterSubscriber.DoesNotExist:
        unsubscribe_url = (
            f"https://gumisofts.com/newsletter/unsubscribe?email={subscriber_email}"
        )

    context = {
        "email": subscriber_email,
        "subscription_date": timezone.now().strftime("%B %d, %Y"),
        "website_url": "https://gumisofts.com",  # Update with actual website URL
        "unsubscribe_url": unsubscribe_url,
    }

    html_message = render_to_string("emails/subscription_confirmation.html", context)
    plain_message = f"""
Hi there!

Thank you for subscribing to the Gumisofts Newsletter! We're excited to have you join our community.

Your subscription has been confirmed:
Email: {subscriber_email}
Subscribed on: {context['subscription_date']}

What you can expect from us:
- Latest updates on our projects and services
- Tech insights and development tips
- Exclusive announcements and early access
- Industry trends and best practices

Visit our website: {context['website_url']}

To unsubscribe: {context['unsubscribe_url']}

Best regards,
Gumisofts Team
"""

    return send_email_to(
        subject="Welcome to Gumisofts Newsletter!",
        message=plain_message,
        to_emails=[subscriber_email],
        html_message=html_message,
    )


def send_admin_subscription_notification(subscriber_email: str, subscriber_id: int):
    """Send notification to admins when new user subscribes"""
    from blog.models import NewsletterSubscriber

    # Get subscription statistics
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = today_start.replace(day=1)

    total_subscribers = NewsletterSubscriber.objects.count()
    new_today = NewsletterSubscriber.objects.filter(created_at__gte=today_start).count()
    new_this_week = NewsletterSubscriber.objects.filter(
        created_at__gte=week_start
    ).count()
    new_this_month = NewsletterSubscriber.objects.filter(
        created_at__gte=month_start
    ).count()

    context = {
        "subscriber_email": subscriber_email,
        "subscriber_id": subscriber_id,
        "subscription_date": now.strftime("%B %d, %Y"),
        "subscription_time": now.strftime("%I:%M %p"),
        "notification_time": now.strftime("%B %d, %Y at %I:%M %p"),
        "total_subscribers": total_subscribers,
        "new_today": new_today,
        "new_this_week": new_this_week,
        "new_this_month": new_this_month,
        "admin_subscribers_url": "https://gumisofts.com/admin/blog/newslettersubscriber/",  # Update with actual admin URL
        "create_newsletter_url": "https://gumisofts.com/admin/newsletter/create/",  # Update with actual URL
    }

    html_message = render_to_string("emails/admin_notification.html", context)
    plain_message = f"""
New Newsletter Subscription - Gumisofts

A new user has subscribed to the newsletter:

Subscriber Details:
- Email: {subscriber_email}
- Date: {context['subscription_date']}
- Time: {context['subscription_time']}
- Subscriber ID: #{subscriber_id}

Current Statistics:
- Total Subscribers: {total_subscribers}
- New Today: {new_today}
- New This Week: {new_this_week}
- New This Month: {new_this_month}

This notification was generated at {context['notification_time']}

Best regards,
Gumisofts Newsletter System
"""

    return send_email_to_admins(
        subject=f"New Newsletter Subscription: {subscriber_email}",
        message=plain_message,
        html_message=html_message,
    )


def send_newsletter_to_subscribers(
    subject: str,
    newsletter_content: str = None,
    featured_post=None,
    recent_posts=None,
    **kwargs,
):
    """Send newsletter to all subscribers"""
    from blog.models import BlogPost, NewsletterSubscriber

    # Get all active subscribers
    subscribers = NewsletterSubscriber.objects.all().values_list("email", flat=True)

    if not subscribers:
        return False

    # Prepare context for the newsletter
    context = {
        "subject": subject,
        "newsletter_date": timezone.now().strftime("%B %d, %Y"),
        "newsletter_content": newsletter_content,
        "featured_post": featured_post,
        "recent_posts": recent_posts or [],
        "show_stats": kwargs.get("show_stats", True),
        "total_posts": BlogPost.objects.filter(status="published").count(),
        "total_subscribers": len(subscribers),
        "total_views": sum(
            BlogPost.objects.filter(status="published").values_list("views", flat=True)
        ),
        "website_url": "https://gumisofts.com",
        "blog_url": "https://gumisofts.com/blog",
        "portfolio_url": "https://gumisofts.com/portfolio",
        "contact_url": "https://gumisofts.com/contact",
        "linkedin_url": "https://linkedin.com/company/gumisofts",
        "twitter_url": "https://twitter.com/gumisofts",
        "github_url": "https://github.com/gumisofts",
        "unsubscribe_url": "https://gumisofts.com/newsletter/unsubscribe",
        "preferences_url": "https://gumisofts.com/newsletter/preferences",
    }

    html_message = render_to_string("emails/newsletter.html", context)
    plain_message = f"""
{subject}
{context['newsletter_date']}

{newsletter_content or ''}

Featured Article:
{featured_post.get('title', '') if featured_post else 'No featured post'}

Recent Articles:
{chr(10).join([f"- {post.get('title', '')}" for post in recent_posts]) if recent_posts else 'No recent posts'}

Visit our website: {context['website_url']}
Unsubscribe: {context['unsubscribe_url']}

Best regards,
Gumisofts Team
"""

    # Send to all subscribers
    return send_email_to(
        subject=subject,
        message=plain_message,
        to_emails=list(subscribers),
        html_message=html_message,
    )


def send_job_application_confirmation(application):
    """Send confirmation email to job applicant"""
    from jobs.models import JobApplication

    # Prepare job details
    job = application.job
    salary_str = ""
    if job.salary:
        salary_str = f"{job.salary.min:,} - {job.salary.max:,} {job.salary.currency}"

    context = {
        "applicant_name": application.full_name,
        "applicant_email": application.email,
        "job_title": job.title,
        "job_id": job.id,
        "job_category": job.category,
        "job_type": job.get_type_display(),
        "job_location": job.location,
        "job_salary": salary_str,
        "application_date": application.applied_date.strftime("%B %d, %Y"),
        "application_id": application.id,
        "linkedin_profile": application.linkedin,
        "cover_letter": bool(application.cover_letter),
        "job_description_url": f"https://gumisofts.com/jobs/{job.id}/",  # Update with actual URL
        "company_careers_url": "https://gumisofts.com/careers/",
        "linkedin_url": "https://linkedin.com/company/gumisofts",
        "twitter_url": "https://twitter.com/gumisofts",
        "github_url": "https://github.com/gumisofts",
    }

    html_message = render_to_string("emails/job_application_confirmation.html", context)
    plain_message = f"""
Dear {application.full_name},

Thank you for your application for the {job.title} position at Gumisofts!

Application Details:
- Position: {job.title}
- Job ID: {job.id}
- Application Date: {context['application_date']}
- Application ID: #{application.id}

Your application has been successfully submitted and our hiring team will review it carefully.

What happens next:
1. Our team will review your application within 3-5 business days
2. If your profile matches our requirements, we'll contact you for screening
3. Selected candidates will be invited for interviews
4. We'll notify you of our decision regardless of the outcome

You can view the job description at: {context['job_description_url']}

Questions? Contact us at careers@gumisofts.com

Best regards,
Gumisofts Hiring Team
"""

    return send_email_to(
        subject=f"Application Received: {job.title} - Gumisofts",
        message=plain_message,
        to_emails=[application.email],
        html_message=html_message,
    )


def send_admin_job_application_notification(application):
    """Send notification to admins when new job application is received"""
    from django.utils import timezone

    from jobs.models import JobApplication

    job = application.job
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())

    # Calculate statistics
    total_applications = JobApplication.objects.count()
    applications_today = JobApplication.objects.filter(
        applied_date__gte=today_start
    ).count()
    applications_this_week = JobApplication.objects.filter(
        applied_date__gte=week_start
    ).count()
    applications_for_job = JobApplication.objects.filter(job=job).count()
    pending_applications = JobApplication.objects.filter(status="pending").count()

    # Prepare salary string
    salary_str = ""
    if job.salary:
        salary_str = f"{job.salary.min:,} - {job.salary.max:,} {job.salary.currency}"

    # Prepare context
    context = {
        "applicant_name": application.full_name,
        "applicant_email": application.email,
        "linkedin_profile": application.linkedin,
        "cover_letter": application.cover_letter,
        "resume_url": application.resume.url if application.resume else None,
        "application_date": application.applied_date.strftime("%B %d, %Y"),
        "application_id": application.id,
        "job_title": job.title,
        "job_id": job.id,
        "job_category": job.category,
        "job_type": job.get_type_display(),
        "job_location": job.location,
        "job_salary": salary_str,
        "job_deadline": job.deadline.strftime("%B %d, %Y") if job.deadline else None,
        "total_applications": total_applications,
        "applications_today": applications_today,
        "applications_this_week": applications_this_week,
        "applications_for_job": applications_for_job,
        "pending_applications": pending_applications,
        "notification_time": now.strftime("%B %d, %Y at %I:%M %p"),
        "admin_application_url": f"https://gumisofts.com/admin/jobs/jobapplication/{application.id}/change/",  # Update with actual admin URL
        "shortlist_url": f"https://gumisofts.com/admin/jobs/jobapplication/{application.id}/shortlist/",
        "schedule_interview_url": f"https://gumisofts.com/admin/jobs/jobapplication/{application.id}/interview/",
        "reject_url": f"https://gumisofts.com/admin/jobs/jobapplication/{application.id}/reject/",
    }

    html_message = render_to_string(
        "emails/admin_job_application_notification.html", context
    )
    plain_message = f"""
New Job Application - Gumisofts

A new application has been received:

Applicant: {application.full_name}
Email: {application.email}
Position: {job.title}
Application ID: #{application.id}
Date: {context['application_date']}

Job Details:
- Position: {job.title}
- Department: {job.category}
- Type: {job.get_type_display()}
- Location: {job.location}

Statistics:
- Total Applications: {total_applications}
- Applications Today: {applications_today}
- Applications This Week: {applications_this_week}
- For This Position: {applications_for_job}
- Pending Review: {pending_applications}

View application: {context['admin_application_url']}

Generated at {context['notification_time']}
"""

    return send_email_to_admins(
        subject=f"New Job Application: {job.title} - {application.full_name}",
        message=plain_message,
        html_message=html_message,
    )


def send_job_status_update_email(application, old_status, new_status, **kwargs):
    """Send status update email to job applicant"""
    from jobs.models import JobApplication

    job = application.job

    # Prepare context
    context = {
        "applicant_name": application.full_name,
        "status": new_status,
        "job_title": job.title,
        "application_id": application.id,
        "application_date": application.applied_date.strftime("%B %d, %Y"),
        "job_description_url": f"https://gumisofts.com/jobs/{job.id}/",
        "linkedin_url": "https://linkedin.com/company/gumisofts",
        "twitter_url": "https://twitter.com/gumisofts",
        "github_url": "https://github.com/gumisofts",
        "next_steps": True,
    }

    # Add optional context from kwargs
    context.update(kwargs)

    # Determine subject based on status
    subject_map = {
        "shortlisted": f"Great News! You've been shortlisted - {job.title}",
        "rejected": f"Application Update - {job.title}",
        "interview": f"Interview Scheduled - {job.title}",
        "reviewed": f"Application Under Review - {job.title}",
        "offer": f"Job Offer - {job.title} at Gumisofts",
    }

    subject = subject_map.get(new_status, f"Application Status Update - {job.title}")

    html_message = render_to_string("emails/job_status_update.html", context)

    # Create plain text version based on status
    if new_status == "shortlisted":
        plain_message = f"""
Dear {application.full_name},

Congratulations! Your application for {job.title} has been shortlisted for the next round.

Our hiring team was impressed with your application and we would like to move forward with the next stage of our selection process.

We will contact you within 2-3 business days to schedule your interview.

Best regards,
Gumisofts Hiring Team
"""
    elif new_status == "rejected":
        plain_message = f"""
Dear {application.full_name},

Thank you for your interest in the {job.title} position at Gumisofts.

After careful consideration, we have decided to move forward with other candidates for this position. This decision was not easy given the quality of applications we received.

We encourage you to apply for future openings that match your skills and will keep your application in our talent pool for future consideration.

Best regards,
Gumisofts Hiring Team
"""
    elif new_status == "interview":
        interview_details = kwargs.get("interview_details", {})
        interview_info = ""
        if interview_details:
            interview_info = f"""
Interview Details:
Date: {interview_details.get('date', 'TBD')}
Time: {interview_details.get('time', 'TBD')}
Type: {interview_details.get('type', 'TBD')}
Location: {interview_details.get('location', 'TBD')}
"""

        plain_message = f"""
Dear {application.full_name},

We would like to invite you for an interview for the {job.title} position.

{interview_info}

Please confirm your attendance by replying to this email.

Best regards,
Gumisofts Hiring Team
"""
    else:
        plain_message = f"""
Dear {application.full_name},

Your application for {job.title} has been updated.

Current Status: {new_status.title()}
Application ID: #{application.id}

We will keep you updated on any further developments.

Best regards,
Gumisofts Hiring Team
"""

    return send_email_to(
        subject=subject,
        message=plain_message,
        to_emails=[application.email],
        html_message=html_message,
    )


def send_test_email(to_email):
    """Send a test email"""
    send_email_to_admins("Test Email From Gumisofts", "This Only Test Email")

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from core.emails import (
    send_admin_job_application_notification,
    send_job_application_confirmation,
    send_job_status_update_email,
)

from .models import JobApplication

logger = logging.getLogger(__name__)


@receiver(post_save, sender=JobApplication)
def on_job_application_created_or_updated(sender, instance, created, **kwargs):
    """
    Signal handler for job application creation and status updates.
    Sends confirmation email to applicant and notification to admins on creation.
    Sends status update email to applicant when status changes.
    """
    if created:
        try:
            # Send confirmation email to applicant
            send_job_application_confirmation(instance)
            logger.info(
                f"Job application confirmation email sent to {instance.email} for {instance.job.title}"
            )

            # Send notification to admins
            send_admin_job_application_notification(instance)
            logger.info(
                f"Admin notification sent for new job application from {instance.email} for {instance.job.title}"
            )

        except Exception as e:
            logger.error(
                f"Error sending job application emails for {instance.email}: {str(e)}"
            )
            # Continue execution - don't fail the application if emails fail

    else:
        # Handle status updates for existing applications
        try:
            # Get the previous instance to check if status changed
            if hasattr(instance, "_original_status"):
                old_status = instance._original_status
                new_status = instance.status

                if old_status != new_status:
                    # Status has changed, send update email
                    send_job_status_update_email(instance, old_status, new_status)
                    logger.info(
                        f"Status update email sent to {instance.email} for {instance.job.title}: {old_status} -> {new_status}"
                    )

        except Exception as e:
            logger.error(
                f"Error sending job status update email for {instance.email}: {str(e)}"
            )


def send_interview_scheduled_email(application, interview_details):
    """
    Send interview scheduled email with specific details.
    This is called manually when scheduling interviews with specific details.
    """
    try:
        send_job_status_update_email(
            application,
            application.status,
            "interview",
            interview_details=interview_details,
        )
        logger.info(
            f"Interview scheduled email sent to {application.email} for {application.job.title}"
        )
        return True
    except Exception as e:
        logger.error(
            f"Error sending interview scheduled email for {application.email}: {str(e)}"
        )
        return False


def send_offer_email(application, offer_details):
    """
    Send job offer email with specific details.
    This is called manually when extending job offers.
    """
    try:
        send_job_status_update_email(
            application,
            application.status,
            "offer",
            offer_details_link=offer_details.get("offer_link"),
            offer_deadline=offer_details.get("deadline"),
            personal_message=offer_details.get("message"),
        )
        logger.info(
            f"Job offer email sent to {application.email} for {application.job.title}"
        )
        return True
    except Exception as e:
        logger.error(f"Error sending job offer email for {application.email}: {str(e)}")
        return False

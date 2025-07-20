import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from core.emails import (
    send_admin_subscription_notification,
    send_newsletter_subscription_confirmation,
)

from .models import NewsletterSubscriber

logger = logging.getLogger(__name__)


@receiver(post_save, sender=NewsletterSubscriber)
def on_newsletter_subscription(sender, instance, created, **kwargs):
    """
    Signal handler for newsletter subscription.
    Sends confirmation email to subscriber and notification to admins.
    """
    if created and instance.is_active:
        try:
            # Send confirmation email to subscriber
            send_newsletter_subscription_confirmation(instance.email)
            logger.info(f"Subscription confirmation email sent to {instance.email}")

            # Send notification to admins
            send_admin_subscription_notification(instance.email, instance.id)
            logger.info(f"Admin notification sent for new subscriber: {instance.email}")

        except Exception as e:
            logger.error(
                f"Error sending newsletter subscription emails for {instance.email}: {str(e)}"
            )
            # Continue execution - don't fail the subscription if emails fail

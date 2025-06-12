from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Message


@receiver(signal=[post_save], sender=Message)
def on_create_message(sender, instance, created, **kwargs):
    if created:
        #
        pass

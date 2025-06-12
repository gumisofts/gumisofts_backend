from django.conf import settings
from django.core.mail import send_mail


def send_email_to_admins(subject: str, message: str):

    to_emails = list(map(lambda x: x[1], settings.ADMINS))

    return send_email_to(subject=subject, message=message, to_emails=to_emails)


def send_email_to(subject: str, message: str, to_emails: list):

    return send_mail(
        subject,
        message,
        f"Gumisofts <{settings.EMAIL_HOST_USER}> ",
        to_emails,
        fail_silently=False,
    )


def send_test_email(to_email):
    send_email_to_admins("Test Email From Gumisofts", "This Only Test Email")

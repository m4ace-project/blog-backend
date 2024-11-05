from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlencode


def send_verification_email(email, token):

    # Build the verification link
    verification_url = f"{settings.FRONTEND_URL}/api/verify-email/?{urlencode({'token': token})}"

    # Email content
    subject = 'Email Verification'
    message = f"Please click the link to verify your email: {verification_url}"

    # Send the verification email
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    email.send(fail_silently=False)


def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()

    
def send_custom_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()
        
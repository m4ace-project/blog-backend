from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings

def send_otp_email(email, otp):
    subject = "Your Email Verification OTP"
    message = f"Your OTP for email verification is {otp}. This OTP is valid for 10 minutes."
    send_mail(subject, message, 'no-reply@example.com', [email])

def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()

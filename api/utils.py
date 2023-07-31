import smtplib
from django.core.mail import send_mail
from django.conf import settings


class Util:

    @staticmethod
    def send_email(data):
        try:
            send_mail(
                subject=data['email_subject'],
                message=data['email_body'],
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[data['to_email']], fail_silently=False
            )
        except smtplib.SMTPException as e:
            print(f"An error occured: {e}")
        
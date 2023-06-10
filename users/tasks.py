from celery import shared_task
from django.core.mail import send_mail
from AraianaLabsTask import settings
from users.models import User


@shared_task(bind=True)
def send_mail_func(self, subject, message):
    # operations
    users = User.objects.all()
    mail_subject = subject
    message = message
    for user in users:
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
        print(message)
    return "Done"

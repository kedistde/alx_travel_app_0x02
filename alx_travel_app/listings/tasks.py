from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_payment_confirmation_email(to_email):
    send_mail(
        subject="Payment Successful",
        message="Your payment was received successfully. Thank you for booking!",
        from_email="no-reply@alxtravel.com",
        recipient_list=[to_email],
        fail_silently=False,
    )

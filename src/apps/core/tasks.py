"""Tasks."""

from datetime import timedelta, datetime
import cloudinary.uploader
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from src.apps.user_profile.models import UserProfile
from src.apps.booking.models import (Ticket, Reservation)  # noqa: F401


@shared_task(name='automatic-reminder')
def automatic_reminder():
    """Automatic task to remind users of there flight."""

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    re_qs = Reservation.objects.filter(flight__date=tomorrow)
    bo_qs = Ticket.objects.filter(flight__date=tomorrow)

    if re_qs.exists():
        re_data = [(re.made_by.email, re.flight.flight_number, None)
                   for re in re_qs]
        [send_email(email, tomorrow) for email in re_data]

    if bo_qs.exists():
        bo_data = [(
            bo.made_by.email,
            bo.flight.flight_number,
            bo.ticket_ref,
        ) for bo in bo_qs]
        [send_email(email, tomorrow) for email in bo_data]


def send_email(email, date):
    """Send reminder email"""

    ctx = {'flight_number': email[1], 'ticket_ref': email[2], 'date': date}

    subject = 'Reminder'
    template = get_template('reminder_email.html')
    html_content = template.render(ctx)
    send(subject, email[0], html_content)


@shared_task(name='upload-photo')
def upload_image(file, profile_id, photo_public_id, time_stamp):
    """Method to upload image file to cloudinary"""
    try:
        response = cloudinary.uploader.upload(file,
                                              folder=f"airtech/{profile_id}/",
                                              public_id=f"v{time_stamp}",
                                              allowed_formats=['jpg', 'png'],
                                              eager=[{
                                                  "width": 300,
                                                  "height": 300,
                                                  "crop": "mfit"
                                              }])

        if photo_public_id and response:
            # delete the old photo and save a new one.
            cloudinary.uploader.destroy(photo_public_id)
            photo_saved = UserProfile.objects.filter(pk=profile_id).update(
                photo_public_id=response['public_id'],
                photo_url=response['secure_url'])

            if photo_saved:
                print('SEND EMAIL')

    except Exception:
        print('SEND EXCEPTION EMAIL')


@shared_task(name='send-email')
def send(subject, to, content, from_email=None, bcc=None):
    """Method to send out the emails.
    Args:
        subject (str): The subject of the email.
        to (str): The recipient of the email.
        from_email (str): The sender of the email.
        content (html): The email template
        bcc (list|str): The emails for blind copying
    Returns:
        None
    """

    from_email = 'Support <mailgun@sandbox1b552285ba6b49688aac0d7582ec23ff' \
                 '.mailgun.org>' if from_email is None else from_email

    email = EmailMultiAlternatives(
        subject,
        content,
        from_email,
        [to],
        bcc,
        reply_to=['support@airtech-v.herokuapp.com'],
        headers={'Message-ID': 'Important'},
    )
    email.attach_alternative(content, "text/html")
    email.send()

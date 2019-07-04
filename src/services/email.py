"""Module for email concrete"""

from django.core.mail import EmailMultiAlternatives

from src.celery import celery_app


@celery_app.task(name='send-email')
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
        reply_to=['victor.nwokeocha@andela.com'],
        headers={'Message-ID': 'Important'},
    )
    email.attach_alternative(content, "text/html")
    email.send()

from email.message import EmailMessage

from aiosmtplib import SMTP

from src.core import settings


async def send_email(title: str, content: str, recipient_email: str):
    smtp = SMTP(
        hostname=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        start_tls=False,
        use_tls=False,
    )
    await smtp.connect()
    await smtp.starttls()
    await smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_GOOGLE_APP_PASSWORD)

    message = EmailMessage()
    message['From'] = settings.EMAIL_HOST_USER
    message['To'] = recipient_email
    message['Subject'] = title
    message.set_content(content)

    await smtp.send_message(message)
    await smtp.quit()

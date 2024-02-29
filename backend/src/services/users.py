from email.message import EmailMessage
from typing import Optional

from aiosmtplib import SMTP
from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi.requests import Request

from src.core import settings
from src.models import UserModel, get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[UserModel, int]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET

    async def on_after_register(self, user: UserModel, request: Optional[Request] = None):
        pass

    async def on_after_forgot_password(
        self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        await send_email(
            email_content=f'Ваш код для смены пароля: {token}',
            recipient_email=user.email
        )
        # TODO remove print
        print(f'User ID: {user.id}; Verification token: {token}')

    async def on_after_request_verify(
        self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        await send_email(
            email_content=f'Ваш код для подтверждения электронной почты: {token}',
            recipient_email=user.email
        )
        # TODO remove print
        print(f'User ID: {user.id}; Verification token: {token}')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


async def send_email(email_content: str, recipient_email: str, ):
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
    message['Subject'] = 'Регистрация в конструкторе чат-ботов'
    message.set_content(email_content)

    await smtp.send_message(message)
    await smtp.quit()

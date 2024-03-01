from email.message import EmailMessage
from typing import Optional

import jwt
from aiosmtplib import SMTP
from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin, models, exceptions
from fastapi.requests import Request
from fastapi_users.exceptions import FastAPIUsersException
from fastapi_users.jwt import generate_jwt, decode_jwt

from src.core import settings
from src.models import UserModel, get_user_db


class InvalidEmailChangeToken(FastAPIUsersException):
    pass


class AuthService(IntegerIDMixin, BaseUserManager[UserModel, int]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET
    change_email_token_secret = settings.SECRET

    change_email_token_lifetime_seconds: int = 3600
    change_email_token_audience: str = 'fastapi-users:change-email'

    async def on_after_register(self, user: UserModel, request: Optional[Request] = None):
        pass

    async def on_after_forgot_password(
        self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        await send_email(
            title='Смена пароля в конструкторе чат-ботов',
            content=f'Ваш код для смены пароля: {token}',
            recipient_email=user.email
        )
        # TODO remove print
        print(f'User ID: {user.id}; Verification token: {token}')

    async def on_after_request_verify(
        self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        await send_email(
            title='Регистрация в конструкторе чат-ботов',
            content=f'Ваш код для подтверждения электронной почты: {token}',
            recipient_email=user.email
        )
        # TODO remove print
        print(f'User ID: {user.id}; Verification token: {token}')

    async def request_email_change(self, user: models.UP, request: Optional[Request] = None):
        if not user.is_active:
            raise exceptions.UserInactive(
                f'User with ID {user.id} is inactive'
            )

        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "aud": self.change_email_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.change_email_token_secret,
            self.change_email_token_lifetime_seconds,
        )
        await self.on_after_request_email_change(user, token, request)

    async def on_after_request_email_change(
        self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        await send_email(
            title='Смена почты в конструкторе чат-ботов',
            content=f'Ваш код для смены электронной почты: {token}',
            recipient_email=user.email
        )

    async def change_email(
            self, token: str, new_email: str, request: Optional[Request] = None
    ) -> models.UP:
        try:
            data = decode_jwt(
                token,
                self.change_email_token_secret,
                [self.change_email_token_audience],
            )
        except jwt.PyJWTError as e:
            raise InvalidEmailChangeToken(
                f'An error occurred while processing the token: {e}'
            )

        try:
            user_id = data["sub"]
        except KeyError as e:
            raise InvalidEmailChangeToken(
                f'An error occurred while processing the token: {e}'
            )

        try:
            parsed_id = self.parse_id(user_id)
        except exceptions.InvalidID as e:
            raise InvalidEmailChangeToken(
                f'An error occurred while processing the token: {e}'
            )

        user = await self.get(parsed_id)

        if not user.is_active:
            raise exceptions.UserInactive(f'User with ID {user.id} is inactive')

        updated_user = await self._update(user, {"email": new_email})

        return updated_user


async def get_auth_service(user_db=Depends(get_user_db)):
    yield AuthService(user_db)


async def send_email(title: str, content: str, recipient_email: str, ):
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

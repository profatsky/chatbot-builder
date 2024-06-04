import random
from typing import Optional

from async_fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr

from src.core import settings
from src.core.redis import (
    user_ids_to_email_verification_codes, user_ids_to_email_and_change_verification_codes,
    user_ids_to_password_and_change_verification_codes,
)
from src.schemas.auth_schemas import Password
from src.utils import email_utils


async def set_auth_tokens(user_id: int, auth_jwt: AuthJWT):
    access_token = await auth_jwt.create_access_token(subject=user_id)
    refresh_token = await auth_jwt.create_refresh_token(subject=user_id)

    await auth_jwt.set_access_cookies(access_token)
    await auth_jwt.set_refresh_cookies(refresh_token)


async def refresh_access_token(auth_jwt: AuthJWT):
    await auth_jwt.jwt_refresh_token_required()

    user_id = await auth_jwt.get_jwt_subject()
    new_access_token = await auth_jwt.create_access_token(subject=user_id)

    await auth_jwt.set_access_cookies(new_access_token)


async def unset_auth_tokens(auth_jwt: AuthJWT):
    await auth_jwt.jwt_required()
    await auth_jwt.unset_jwt_cookies()


def create_and_save_email_verification_code(user_id: int):
    user_ids_to_email_verification_codes[user_id] = _generate_verification_code()


def get_email_verification_code(user_id: int) -> Optional[int]:
    return user_ids_to_email_verification_codes.get(user_id)


def remove_email_verification_code(user_id: int):
    try:
        del user_ids_to_email_verification_codes[user_id]
    except KeyError:
        pass


def create_and_save_email_change_verification_code(user_id: int, new_email: EmailStr):
    user_ids_to_email_and_change_verification_codes[user_id] = (
        _generate_verification_code(), new_email
    )


def get_email_and_change_verification_code(user_id: int) -> Optional[tuple[int, EmailStr]]:
    return user_ids_to_email_and_change_verification_codes.get(user_id)


def remove_email_change_verification_code(user_id: int):
    try:
        del user_ids_to_email_and_change_verification_codes[user_id]
    except KeyError:
        pass


def _generate_verification_code() -> int:
    return random.randint(100000, 999999)


# TODO replace parameters with UserDTO
async def send_email_with_email_verification(
        user_id: int,
        recipient_email: EmailStr,
        verification_code: int
):
    await email_utils.send_email(
        title='Подтверждение Email',
        content='Для подтверждения Email перейдите по ссылке: '
                f'{settings.CLIENT_APP_URL}/verify-email?user_id={user_id}&code={verification_code}',
        recipient_email=recipient_email
    )


# TODO replace parameters with UserDTO
async def send_email_with_email_change_request(
        user_id: int,
        recipient_email: EmailStr,
        verification_code: int,
        new_email: EmailStr
):
    await email_utils.send_email(
        title='Запрос на смену Email',
        content=f'Для подтверждения смены Email на {new_email} перейдите по ссылке: '
                f'{settings.CLIENT_APP_URL}/verify-email-change?user_id={user_id}&code={verification_code}',
        recipient_email=recipient_email
    )


def create_and_save_password_change_verification_code(user_id: int, new_password: Password):
    user_ids_to_password_and_change_verification_codes[user_id] = (
        _generate_verification_code(), new_password
    )


def get_password_and_change_verification_code(user_id: int) -> Optional[tuple[int, str]]:
    return user_ids_to_password_and_change_verification_codes.get(user_id)


def remove_password_change_verification_code(user_id: int):
    try:
        del user_ids_to_password_and_change_verification_codes[user_id]
    except KeyError:
        pass


async def send_email_with_password_change_request(
        user_id: int,
        recipient_email: EmailStr,
        verification_code: int,
):
    await email_utils.send_email(
        title='Запрос на смену пароля',
        content=f'Для подтверждения смены пароля перейдите по ссылке: '
                f'{settings.CLIENT_APP_URL}/verify-password-change?user_id={user_id}&code={verification_code}',
        recipient_email=recipient_email
    )

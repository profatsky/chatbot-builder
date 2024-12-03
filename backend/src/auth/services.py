import random
from typing import Optional

from pydantic import EmailStr

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.core import settings
from src.core.redis import (
    user_ids_to_email_verification_codes,
    user_ids_to_email_and_change_verification_codes,
    user_ids_to_password_and_change_verification_codes,
)
from src.auth.schemas import Password
from src.users import utils


class AuthService:
    def __init__(self, auth_jwt: AuthJWTDI):
        self._auth_jwt = auth_jwt

    async def set_auth_tokens(self, user_id: int):
        access_token = await self._auth_jwt.create_access_token(subject=user_id)
        refresh_token = await self._auth_jwt.create_refresh_token(subject=user_id)

        await self._auth_jwt.set_access_cookies(access_token)
        await self._auth_jwt.set_refresh_cookies(refresh_token)

    async def refresh_access_token(self):
        await self._auth_jwt.jwt_refresh_token_required()

        user_id = await self._auth_jwt.get_jwt_subject()
        new_access_token = await self._auth_jwt.create_access_token(subject=user_id)

        await self._auth_jwt.set_access_cookies(new_access_token)

    async def unset_auth_tokens(self):
        await self._auth_jwt.jwt_required()
        await self._auth_jwt.unset_jwt_cookies()

    def create_and_save_email_verification_code(self, user_id: int):
        user_ids_to_email_verification_codes[user_id] = self._generate_verification_code()

    def get_email_verification_code(self, user_id: int) -> Optional[int]:
        return user_ids_to_email_verification_codes.get(user_id)

    def remove_email_verification_code(self, user_id: int):
        try:
            del user_ids_to_email_verification_codes[user_id]
        except KeyError:
            pass

    def create_and_save_email_change_verification_code(self, user_id: int, new_email: EmailStr):
        user_ids_to_email_and_change_verification_codes[user_id] = (
            self._generate_verification_code(), new_email
        )

    def get_email_and_change_verification_code(self, user_id: int) -> Optional[tuple[int, EmailStr]]:
        return user_ids_to_email_and_change_verification_codes.get(user_id)

    def remove_email_change_verification_code(self, user_id: int):
        try:
            del user_ids_to_email_and_change_verification_codes[user_id]
        except KeyError:
            pass

    def _generate_verification_code(self) -> int:
        return random.randint(100000, 999999)

    # TODO replace parameters with UserDTO
    async def send_email_with_email_verification(
            self,
            user_id: int,
            recipient_email: EmailStr,
            verification_code: int
    ):
        await utils.send_email(
            title='Подтверждение Email',
            content='Для подтверждения Email перейдите по ссылке: '
                    f'{settings.CLIENT_APP_URL}/verify-email?user_id={user_id}&code={verification_code}',
            recipient_email=recipient_email
        )

    # TODO replace parameters with UserDTO
    async def send_email_with_email_change_request(
            self,
            user_id: int,
            recipient_email: EmailStr,
            verification_code: int,
            new_email: EmailStr
    ):
        await utils.send_email(
            title='Запрос на смену Email',
            content=f'Для подтверждения смены Email на {new_email} перейдите по ссылке: '
                    f'{settings.CLIENT_APP_URL}/verify-email-change?user_id={user_id}&code={verification_code}',
            recipient_email=recipient_email
        )

    def create_and_save_password_change_verification_code(self, user_id: int, new_password: Password):
        user_ids_to_password_and_change_verification_codes[user_id] = (
            self._generate_verification_code(), new_password
        )

    def get_password_and_change_verification_code(self, user_id: int) -> Optional[tuple[int, str]]:
        return user_ids_to_password_and_change_verification_codes.get(user_id)

    def remove_password_change_verification_code(self, user_id: int):
        try:
            del user_ids_to_password_and_change_verification_codes[user_id]
        except KeyError:
            pass

    async def send_email_with_password_change_request(
            self,
            user_id: int,
            recipient_email: EmailStr,
            verification_code: int,
    ):
        await utils.send_email(
            title='Запрос на смену пароля',
            content=f'Для подтверждения смены пароля перейдите по ссылке: '
                    f'{settings.CLIENT_APP_URL}/verify-password-change?user_id={user_id}&code={verification_code}',
            recipient_email=recipient_email
        )

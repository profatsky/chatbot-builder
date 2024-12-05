from pydantic import EmailStr

from src.auth.schemas import AuthCredentialsSchema, Password
from src.users.dependencies.repositories_dependencies import UserRepositoryDI
from src.users.exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError
from src.users.schemas import UserReadSchema, UserWithStatsReadSchema


class UserService:
    def __init__(self, user_repository: UserRepositoryDI):
        self._user_repository = user_repository

    async def create_user(
            self,
            credentials: AuthCredentialsSchema,
    ) -> UserReadSchema:
        user = await self._user_repository.create_user(credentials)
        if user is None:
            raise UserAlreadyExistsError
        return user

    async def get_user_by_email(
            self,
            email: EmailStr,
    ) -> UserReadSchema:
        user = await self._user_repository.get_user_by_email(email)
        if user is None:
            raise UserNotFoundError
        return user

    async def get_user_by_credentials(
            self,
            credentials: AuthCredentialsSchema,
    ) -> UserReadSchema:
        user = await self._user_repository.get_user_by_credentials(credentials)
        if user is None:
            raise InvalidCredentialsError
        return user

    async def set_verified_status_for_user(
            self,
            user_id: int,
    ) -> UserReadSchema:
        user = await self._user_repository.set_verified_status_for_user(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    async def change_user_email_and_set_unverified_status(
            self,
            user_id: int,
            new_email: EmailStr,
    ) -> UserReadSchema:
        user = await self._user_repository.change_user_email_and_set_unverified_status(
            user_id=user_id,
            new_email=new_email,
        )
        if not user:
            raise UserNotFoundError
        return user

    async def get_user_by_id(
            self,
            user_id: int,
    ) -> UserReadSchema:
        user = await self._user_repository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    async def change_user_password(
            self,
            user_id: int,
            new_password: Password,
    ) -> UserReadSchema:
        user = await self._user_repository.change_user_password(
            user_id=user_id,
            new_password=new_password
        )
        if user is None:
            raise UserNotFoundError
        return user

    async def get_user_with_stats(
            self,
            user_id: int,
    ) -> UserWithStatsReadSchema:
        user = await self._user_repository.get_user_with_stats(user_id)
        if user is None:
            raise UserNotFoundError
        return user

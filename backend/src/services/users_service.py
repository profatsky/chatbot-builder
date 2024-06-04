from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence import users_persistence
from src.schemas.auth_schemas import AuthCredentialsSchema, Password
from src.schemas.users_schemas import UserReadSchema, UserWithStatsReadSchema
from src.services.exceptions import users_exceptions


async def create_user(
        credentials: AuthCredentialsSchema,
        session: AsyncSession,
) -> UserReadSchema:
    user = await users_persistence.create_user(credentials, session)
    if user is None:
        raise users_exceptions.UserAlreadyExists
    return user


async def get_user_by_email(
        email: EmailStr,
        session: AsyncSession,
) -> UserReadSchema:
    user = await users_persistence.get_user_by_email(email, session)
    if user is None:
        raise users_exceptions.UserNotFound
    return user


async def get_user_by_credentials(
        credentials: AuthCredentialsSchema,
        session: AsyncSession,
) -> UserReadSchema:
    user = await users_persistence.get_user_by_credentials(credentials, session)
    if user is None:
        raise users_exceptions.InvalidCredentials
    return user


async def set_verified_status_for_user(
        user_id: int,
        session: AsyncSession,
) -> UserReadSchema:
    user = await users_persistence.set_verified_status_for_user(user_id, session)
    if user is None:
        raise users_exceptions.UserNotFound
    return user


async def change_user_email_and_set_unverified_status(
        user_id: int,
        new_email: EmailStr,
        session: AsyncSession,
) -> UserReadSchema:
    user = await users_persistence.change_user_email_and_set_unverified_status(
        user_id, new_email, session
    )
    if not user:
        raise users_exceptions.UserNotFound
    return user


async def get_user_by_id(
        user_id: int,
        session: AsyncSession,
) -> UserReadSchema:
    user = await users_persistence.get_user_by_id(user_id, session)
    if user is None:
        raise users_exceptions.UserNotFound
    return user


async def change_user_password(
        user_id: int,
        new_password: Password,
        session: AsyncSession,
) -> UserReadSchema:
    user = await users_persistence.change_user_password(user_id, new_password, session)
    if user is None:
        raise users_exceptions.UserNotFound
    return user


async def get_user_with_stats(
        user_id: int,
        session: AsyncSession,
) -> UserWithStatsReadSchema:
    user = await users_persistence.get_user_with_stats(user_id, session)
    if user is None:
        raise users_exceptions.UserNotFound
    return user

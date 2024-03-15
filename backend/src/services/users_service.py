from typing import Optional

from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserModel
from src.schemas.auth_schemas import AuthCredentialsSchema, Password


async def create_new_user(
        credentials: AuthCredentialsSchema,
        session: AsyncSession,
) -> Optional[UserModel]:
    user = UserModel(
        email=credentials.email,
        hashed_password=_hash_password(credentials.password)
    )
    try:
        session.add(user)
        await session.commit()
    except IntegrityError:
        return

    return user


async def get_user_by_email(
        email: EmailStr,
        session: AsyncSession,
) -> Optional[UserModel]:
    user = await session.execute(
        select(UserModel)
        .where(
            UserModel.email == email,
        )
    )
    user = user.scalar()
    return user


async def get_user_by_credentials(
        credentials: AuthCredentialsSchema,
        session: AsyncSession,
) -> Optional[UserModel]:
    user = await get_user_by_email(credentials.email, session)

    if not user or not _verify_password(credentials.password, user.hashed_password):
        return

    return user


def _verify_password(plain_password: Password, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)


def _hash_password(password: Password) -> str:
    return bcrypt.hash(password)


async def set_verified_status_for_user(
        user_id: int,
        session: AsyncSession,
) -> Optional[UserModel]:
    user = await get_user_by_id(user_id, session)
    if user is None:
        return

    user.is_verified = True
    await session.commit()

    return user


async def change_user_email_and_set_unverified_status(
        user_id: int,
        new_email: EmailStr,
        session: AsyncSession,
) -> Optional[UserModel]:
    user = await get_user_by_id(user_id, session)
    if user is None:
        return

    user.email = new_email
    user.is_verified = False
    await session.commit()

    return user


async def get_user_by_id(
        user_id: int,
        session: AsyncSession,
) -> Optional[UserModel]:
    user = await session.execute(
        select(UserModel)
        .where(UserModel.user_id == user_id)
    )
    user = user.scalar()
    return user


async def change_user_password(
        user_id: int,
        new_password: Password,
        session: AsyncSession,
) -> Optional[UserModel]:
    user = await get_user_by_id(user_id, session)
    if user is None:
        return

    user.hashed_password = _hash_password(new_password)
    await session.commit()

    return user

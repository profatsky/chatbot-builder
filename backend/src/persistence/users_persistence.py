from typing import Optional

from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserModel, ProjectModel
from src.schemas.auth_schemas import AuthCredentialsSchema, Password
from src.schemas.users_schemas import UserReadSchema, UserWithStatsReadSchema


async def create_user(
        credentials: AuthCredentialsSchema,
        session: AsyncSession,
) -> Optional[UserReadSchema]:
    user = UserModel(
        email=credentials.email,
        hashed_password=_hash_password(credentials.password)
    )
    try:
        session.add(user)
        await session.commit()
    except IntegrityError:
        return

    return UserReadSchema.model_validate(user)


def _hash_password(password: Password) -> str:
    return bcrypt.hash(password)


async def get_user_by_email(
        email: EmailStr,
        session: AsyncSession,
) -> Optional[UserReadSchema]:
    user = await _get_user_by_email(email, session)
    if user is None:
        return
    return UserReadSchema.model_validate(user)


async def _get_user_by_email(
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
) -> Optional[UserReadSchema]:
    user = await _get_user_by_email(credentials.email, session)
    if user is None or not _verify_password(credentials.password, user.hashed_password):
        return
    return UserReadSchema.model_validate(user)


def _verify_password(plain_password: Password, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)


async def get_user_by_id(
        user_id: int,
        session: AsyncSession,
) -> Optional[UserReadSchema]:
    user = await _get_user_by_id(user_id, session)
    if user is None:
        return
    return UserReadSchema.model_validate(user)


async def _get_user_by_id(
        user_id: int,
        session: AsyncSession,
) -> Optional[UserModel]:
    user = await session.execute(
        select(UserModel)
        .where(UserModel.user_id == user_id)
    )
    user = user.scalar()
    return user


async def set_verified_status_for_user(
        user_id: int,
        session: AsyncSession,
) -> Optional[UserReadSchema]:
    user = await _get_user_by_id(user_id, session)
    if user is None:
        return

    user.is_verified = True
    await session.commit()

    return UserReadSchema.model_validate(user)


async def change_user_email_and_set_unverified_status(
        user_id: int,
        new_email: EmailStr,
        session: AsyncSession,
) -> Optional[UserReadSchema]:
    user = await _get_user_by_id(user_id, session)
    if user is None:
        return

    user.email = new_email
    user.is_verified = False
    await session.commit()

    return UserReadSchema.model_validate(user)


async def change_user_password(
        user_id: int,
        new_password: Password,
        session: AsyncSession,
) -> Optional[UserReadSchema]:
    user = await _get_user_by_id(user_id, session)
    if user is None:
        return

    user.hashed_password = _hash_password(new_password)
    await session.commit()

    return UserReadSchema.model_validate(user)


async def get_user_with_stats(
        user_id: int,
        session: AsyncSession,
) -> Optional[UserWithStatsReadSchema]:
    query = (
        session.sync_session.query(
            UserModel,
            func.count(ProjectModel.project_id).label('project_count')
        )
        .outerjoin(UserModel.projects)
        .where(UserModel.user_id == user_id)
        .group_by(UserModel.user_id)
    )
    result = await session.execute(query)
    user, project_count = result.first()

    return UserWithStatsReadSchema(**user.__dict__, project_count=project_count)

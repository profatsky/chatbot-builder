from typing import Optional

from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from src.auth.schemas import AuthCredentialsSchema, Password
from src.core.dependencies.db_dependencies import AsyncSessionDI
from src.projects.models import ProjectModel
from src.users.models import UserModel
from src.users.schemas import UserReadSchema, UserWithStatsReadSchema


class UserRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def create_user(
            self,
            credentials: AuthCredentialsSchema,
    ) -> Optional[UserReadSchema]:
        user = UserModel(
            email=credentials.email,
            hashed_password=self._hash_password(credentials.password)
        )
        try:
            self._session.add(user)
            await self._session.commit()
        except IntegrityError:
            return

        return UserReadSchema.model_validate(user)

    @staticmethod
    def _hash_password(password: Password) -> str:
        return bcrypt.hash(password)

    async def get_user_by_email(
            self,
            email: EmailStr,
    ) -> Optional[UserReadSchema]:
        user = await self._get_user_by_email(email)
        if user is None:
            return
        return UserReadSchema.model_validate(user)

    async def _get_user_by_email(
            self,
            email: EmailStr,
    ) -> Optional[UserModel]:
        user = await self._session.execute(
            select(UserModel)
            .where(
                UserModel.email == email,
            )
        )
        user = user.scalar()
        return user

    async def get_user_by_credentials(
            self,
            credentials: AuthCredentialsSchema,
    ) -> Optional[UserReadSchema]:
        user = await self._get_user_by_email(credentials.email)
        if user is None or not self._verify_password(credentials.password, user.hashed_password):
            return
        return UserReadSchema.model_validate(user)

    @staticmethod
    def _verify_password(
            plain_password: Password,
            hashed_password: str,
    ) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    async def get_user_by_id(
            self,
            user_id: int,
    ) -> Optional[UserReadSchema]:
        user = await self._get_user_by_id(user_id)
        if user is None:
            return
        return UserReadSchema.model_validate(user)

    async def _get_user_by_id(
            self,
            user_id: int,
    ) -> Optional[UserModel]:
        user = await self._session.execute(
            select(UserModel)
            .where(UserModel.user_id == user_id)
        )
        user = user.scalar()
        return user

    async def set_verified_status_for_user(
            self,
            user_id: int,
    ) -> Optional[UserReadSchema]:
        user = await self._get_user_by_id(user_id)
        if user is None:
            return

        user.is_verified = True
        await self._session.commit()

        return UserReadSchema.model_validate(user)

    async def change_user_email_and_set_unverified_status(
            self,
            user_id: int,
            new_email: EmailStr,
    ) -> Optional[UserReadSchema]:
        user = await self._get_user_by_id(user_id)
        if user is None:
            return

        user.email = new_email
        user.is_verified = False
        await self._session.commit()

        return UserReadSchema.model_validate(user)

    async def change_user_password(
            self,
            user_id: int,
            new_password: Password,
    ) -> Optional[UserReadSchema]:
        user = await self._get_user_by_id(user_id)
        if user is None:
            return

        user.hashed_password = self._hash_password(new_password)
        await self._session.commit()

        return UserReadSchema.model_validate(user)

    async def get_user_with_stats(
            self,
            user_id: int,
    ) -> Optional[UserWithStatsReadSchema]:
        query = (
            self._session.sync_session.query(
                UserModel,
                func.count(ProjectModel.project_id).label('project_count')
            )
            .outerjoin(UserModel.projects)
            .where(UserModel.user_id == user_id)
            .group_by(UserModel.user_id)
        )
        result = await self._session.execute(query)
        user, project_count = result.first()

        return UserWithStatsReadSchema(
            **user.__dict__,
            project_count=project_count
        )

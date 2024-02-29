import datetime

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import Integer, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base, get_async_session


class UserModel(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column('user_id', Integer, primary_key=True)
    registered_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserModel)

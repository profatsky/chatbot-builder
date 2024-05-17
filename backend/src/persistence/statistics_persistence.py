from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserModel, ProjectModel


async def count_users(session: AsyncSession) -> int:
    user_count = await session.scalar(
        select(func.count()).select_from(UserModel)
    )
    return user_count


async def count_projects(session: AsyncSession) -> int:
    project_count = await session.scalar(
        select(func.count()).select_from(ProjectModel)
    )
    return project_count

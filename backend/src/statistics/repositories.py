from sqlalchemy import func, select

from src.core.dependencies.db_dependencies import AsyncSessionDI
from src.projects.models import ProjectModel
from src.users.models import UserModel


class StatisticRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def count_users(self) -> int:
        user_count = await self._session.scalar(
            select(func.count()).select_from(UserModel)
        )
        return user_count

    async def count_projects(self) -> int:
        project_count = await self._session.scalar(
            select(func.count()).select_from(ProjectModel)
        )
        return project_count

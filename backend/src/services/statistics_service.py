from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence import statistics_persistence
from src.schemas.statistics_schemas import StatisticSchema
from src.services import users_service
from src.services.exceptions import users_exceptions


async def check_access_and_get_statistic(user_id: int, session: AsyncSession) -> StatisticSchema:
    user = await users_service.get_user_by_id(user_id, session)
    if user is None or not user.is_superuser:
        raise users_exceptions.UserDoesNotHavePermission

    user_count = await _count_users(session)
    project_count = await _count_projects(session)

    return StatisticSchema(user_count=user_count, project_count=project_count)


async def _count_users(session: AsyncSession) -> int:
    user_count = await statistics_persistence.count_users(session)
    return user_count


async def _count_projects(session: AsyncSession) -> int:
    project_count = await statistics_persistence.count_projects(session)
    return project_count

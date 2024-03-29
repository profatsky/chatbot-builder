from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence import plugins_persistence
from src.schemas.plugins_schemas import PluginReadSchema

PLUGINS_PER_PAGE = 9


async def get_plugins(
        page: int,
        session: AsyncSession,
) -> list[PluginReadSchema]:
    plugins = await plugins_persistence.get_plugins(
        offset=page * PLUGINS_PER_PAGE,
        limit=PLUGINS_PER_PAGE,
        session=session,
    )
    return plugins

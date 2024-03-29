from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.plugins import PluginModel
from src.schemas.plugins_schemas import PluginReadSchema


async def get_plugins(
        offset: int,
        limit: int,
        session: AsyncSession
) -> list[PluginReadSchema]:
    plugins = await session.execute(
        select(PluginModel)
        .order_by(PluginModel.created_at)
        .offset(offset)
        .limit(limit)
    )
    plugins = plugins.scalars().all()
    return [PluginReadSchema.model_validate(plugin) for plugin in plugins]

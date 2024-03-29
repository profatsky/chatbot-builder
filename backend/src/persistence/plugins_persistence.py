from typing import Optional

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.plugins import PluginModel, projects_plugins
from src.schemas.plugins_schemas import PluginReadSchema, PluginCreateSchema


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


async def get_plugin(
        plugin_id: int,
        session: AsyncSession,
) -> Optional[PluginReadSchema]:
    plugin = await session.execute(
        select(PluginModel)
        .where(PluginModel.plugin_id == plugin_id)
    )
    plugin = plugin.scalar()
    return plugin


async def create_plugin(
        plugin_data: PluginCreateSchema,
        session: AsyncSession
) -> PluginReadSchema:
    plugin = PluginModel(**plugin_data.model_dump())
    session.add(plugin)
    await session.commit()
    return PluginReadSchema.model_validate(plugin)


async def delete_plugin(
        plugin_id: int,
        session: AsyncSession,
):
    await session.execute(
        delete(PluginModel)
        .where(PluginModel.plugin_id == plugin_id)
    )
    await session.commit()


async def add_plugin_to_project(
        project_id: int,
        plugin_id: int,
        session: AsyncSession,
):
    await session.execute(
        insert(projects_plugins)
        .values(project_id=project_id, plugin_id=plugin_id)
    )
    await session.commit()


async def remove_plugin_from_project(
        project_id: int,
        plugin_id: int,
        session: AsyncSession,
):
    await session.execute(
        delete(projects_plugins)
        .where(
            projects_plugins.c.project_id == project_id,
            projects_plugins.c.plugin_id == plugin_id,
        )
    )
    await session.commit()

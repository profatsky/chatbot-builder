from typing import Optional

from sqlalchemy import select, insert, delete

from src.core.dependencies.db_dependencies import AsyncSessionDI
from src.plugins.models import PluginModel, projects_plugins
from src.plugins.schemas import PluginReadSchema, PluginCreateSchema


class PluginRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def get_plugins(
            self,
            offset: int,
            limit: int,
    ) -> list[PluginReadSchema]:
        plugins = await self._session.execute(
            select(PluginModel)
            .order_by(PluginModel.created_at)
            .offset(offset)
            .limit(limit)
        )
        plugins = plugins.scalars().all()
        return [PluginReadSchema.model_validate(plugin) for plugin in plugins]

    async def get_plugin(
            self,
            plugin_id: int,
    ) -> Optional[PluginReadSchema]:
        plugin = await self._session.execute(
            select(PluginModel)
            .where(PluginModel.plugin_id == plugin_id)
        )
        plugin = plugin.scalar()
        return plugin

    async def create_plugin(
            self,
            plugin_data: PluginCreateSchema,
    ) -> PluginReadSchema:
        plugin = PluginModel(**plugin_data.model_dump())
        self._session.add(plugin)
        await self._session.commit()
        return PluginReadSchema.model_validate(plugin)

    async def delete_plugin(self, plugin_id: int):
        await self._session.execute(
            delete(PluginModel)
            .where(PluginModel.plugin_id == plugin_id)
        )
        await self._session.commit()

    async def add_plugin_to_project(
            self,
            project_id: int,
            plugin_id: int,
    ):
        await self._session.execute(
            insert(projects_plugins)
            .values(project_id=project_id, plugin_id=plugin_id)
        )
        await self._session.commit()

    async def remove_plugin_from_project(
            self,
            project_id: int,
            plugin_id: int,
    ):
        await self._session.execute(
            delete(projects_plugins)
            .where(
                projects_plugins.c.project_id == project_id,
                projects_plugins.c.plugin_id == plugin_id,
            )
        )
        await self._session.commit()

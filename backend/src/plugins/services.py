from sqlalchemy.ext.asyncio import AsyncSession

from src.plugins.schemas import PluginReadSchema, PluginCreateSchema
from src.projects.schemas import ProjectReadSchema
from src.users import exceptions as users_exceptions
from src.plugins import exceptions as plugins_exceptions
from src.plugins import repositories as plugins_persistence
from src.projects import services as projects_service
from src.users import services as users_service

PLUGINS_PER_PAGE = 9


async def get_plugins(
        page: int,
        session: AsyncSession,
) -> list[PluginReadSchema]:
    plugins = await plugins_persistence.get_plugins(
        offset=(page - 1) * PLUGINS_PER_PAGE,
        limit=PLUGINS_PER_PAGE,
        session=session,
    )
    return plugins


async def get_plugin(
        plugin_id: int,
        session: AsyncSession,
) -> PluginReadSchema:
    plugin = await plugins_persistence.get_plugin(plugin_id, session)
    if plugin is None:
        raise plugins_exceptions.PluginNotFound

    return plugin


async def check_access_and_create_plugin(
        user_id: int,
        plugin_data: PluginCreateSchema,
        session: AsyncSession,
) -> PluginReadSchema:
    user = await users_service.get_user_by_id(user_id, session)
    if user is None or not user.is_superuser:
        raise users_exceptions.UserDoesNotHavePermission

    plugin = await plugins_persistence.create_plugin(plugin_data, session)
    return plugin


async def check_access_and_delete_plugin(
        user_id: int,
        plugin_id: int,
        session: AsyncSession,
):
    user = await users_service.get_user_by_id(user_id, session)
    if user is None or not user.is_superuser:
        raise users_exceptions.UserDoesNotHavePermission

    await plugins_persistence.delete_plugin(plugin_id, session)


async def check_access_and_add_plugin_to_project(
        user_id: int,
        project_id: int,
        plugin_id: int,
        session: AsyncSession,
) -> PluginReadSchema:
    project = await projects_service.check_access_and_get_project(
        user_id=user_id,
        project_id=project_id,
        session=session
    )

    if _project_contain_plugin_with_specified_id(project, plugin_id):
        raise plugins_exceptions.PluginAlreadyInProject

    _ = await get_plugin(plugin_id, session)

    # TODO add a limit on the number of plugins in a project
    plugin = await plugins_persistence.add_plugin_to_project(project_id, plugin_id, session)
    return plugin


async def check_access_and_remove_plugin_from_project(
        user_id: int,
        project_id: int,
        plugin_id: int,
        session: AsyncSession,
):
    project = await projects_service.check_access_and_get_project(
        user_id=user_id,
        project_id=project_id,
        session=session
    )

    if not _project_contain_plugin_with_specified_id(project, plugin_id):
        raise plugins_exceptions.PluginIsNotInProject

    await plugins_persistence.remove_plugin_from_project(project_id, plugin_id, session)


def _project_contain_plugin_with_specified_id(project: ProjectReadSchema, plugin_id: int) -> bool:
    project_plugins_ids = [plugin.plugin_id for plugin in project.plugins]
    return plugin_id in project_plugins_ids

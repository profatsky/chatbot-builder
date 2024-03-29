from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence import projects_persistence
from src.schemas.projects_schemas import (
    ProjectWithDialoguesReadSchema,
    ProjectWithDialoguesAndBlocksReadSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectWithPluginsReadSchema,
)
from src.services.exceptions.projects_exceptions import ProjectNotFound, NoPermissionForProject


async def create_project(
        user_id: int,
        project_data: ProjectCreateSchema,
        session: AsyncSession,
) -> ProjectWithDialoguesReadSchema:
    project = await projects_persistence.create_project(user_id, project_data, session)
    return project


async def get_projects(user_id: int, session: AsyncSession) -> list[ProjectWithDialoguesReadSchema]:
    projects = await projects_persistence.get_projects_with_dialogues(user_id, session)
    return projects


async def check_access_and_get_project_with_dialogues_and_blocks(
        user_id: int,
        project_id: int,
        session: AsyncSession
) -> Optional[ProjectWithDialoguesAndBlocksReadSchema]:
    project = await projects_persistence.get_project_with_dialogues_and_blocks(project_id, session)
    if project is None:
        raise ProjectNotFound

    if project.user_id != user_id:
        raise NoPermissionForProject

    return project


async def check_access_and_get_project_with_dialogues(
        user_id: int,
        project_id: int,
        session: AsyncSession
) -> ProjectWithDialoguesReadSchema:
    project = await projects_persistence.get_project_with_dialogues(project_id, session)
    if project is None:
        raise ProjectNotFound

    if project.user_id != user_id:
        raise NoPermissionForProject

    return project


async def check_access_and_get_project_with_plugins(
        user_id: int,
        project_id: int,
        session: AsyncSession
) -> ProjectWithPluginsReadSchema:
    project = await projects_persistence.get_project_with_plugins(project_id, session)
    if project is None:
        raise ProjectNotFound

    if project.user_id != user_id:
        raise NoPermissionForProject

    return project


async def check_access_and_update_project(
        user_id: int,
        project_id: int,
        project_data: ProjectUpdateSchema,
        session: AsyncSession,
) -> Optional[ProjectWithDialoguesReadSchema]:
    _ = await check_access_and_get_project_with_dialogues(user_id, project_id, session)
    project = await projects_persistence.update_project(project_id, project_data, session)
    return project


async def delete_project(user_id: int, project_id: int, session: AsyncSession):
    _ = await check_access_and_get_project_with_dialogues(user_id, project_id, session)
    await projects_persistence.delete_project(project_id, session)

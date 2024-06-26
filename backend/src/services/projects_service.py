import os
import shutil
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence import projects_persistence
from src.schemas.projects_schemas import (
    ProjectReadSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectToGenerateCodeReadSchema,
)
from src.services.exceptions.projects_exceptions import ProjectNotFound, NoPermissionForProject, ProjectsLimitExceeded


async def create_project(
        user_id: int,
        project_data: ProjectCreateSchema,
        session: AsyncSession,
) -> ProjectReadSchema:
    project_count = await projects_persistence.count_projects(user_id, session)
    if project_count >= 5:
        raise ProjectsLimitExceeded

    project = await projects_persistence.create_project(user_id, project_data, session)
    return project


async def get_projects(user_id: int, session: AsyncSession) -> list[ProjectReadSchema]:
    projects = await projects_persistence.get_projects(user_id, session)
    return projects


async def check_access_and_get_project_to_generate_code(
        user_id: int,
        project_id: int,
        session: AsyncSession
) -> Optional[ProjectToGenerateCodeReadSchema]:
    project = await projects_persistence.get_project_to_generate_code(project_id, session)
    if project is None:
        raise ProjectNotFound

    if project.user_id != user_id:
        raise NoPermissionForProject

    return project


async def check_access_and_get_project(
        user_id: int,
        project_id: int,
        session: AsyncSession
) -> ProjectReadSchema:
    project = await projects_persistence.get_project(project_id, session)
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
) -> Optional[ProjectReadSchema]:
    _ = await check_access_and_get_project(user_id, project_id, session)
    project = await projects_persistence.update_project(project_id, project_data, session)
    return project


async def delete_project(user_id: int, project_id: int, session: AsyncSession):
    _ = await check_access_and_get_project(user_id, project_id, session)

    media_dir_path = os.path.join(
        'src', 'media', 'users', str(user_id), 'projects', str(project_id)
    )
    if os.path.exists(media_dir_path):
        shutil.rmtree(media_dir_path)

    await projects_persistence.delete_project(project_id, session)

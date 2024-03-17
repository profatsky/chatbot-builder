from collections.abc import Sequence
from typing import Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.projects import ProjectModel
from src.schemas.projects_schemas import ProjectCreateSchema, ProjectUpdateSchema


async def create_project(
        user_id: int,
        project_data: ProjectCreateSchema,
        session: AsyncSession,
) -> ProjectModel:
    project = ProjectModel(**project_data.model_dump(), user_id=user_id)
    session.add(project)
    await session.commit()
    return project


async def get_projects(
        user_id: int,
        session: AsyncSession,
) -> Sequence[ProjectModel]:
    projects = await session.execute(
        select(ProjectModel)
        .where(ProjectModel.user_id == user_id)
    )
    projects = projects.scalars().all()
    return projects


async def update_project(
        user_id: int,
        project_id: int,
        project_data: ProjectUpdateSchema,
        session: AsyncSession,
) -> Optional[ProjectModel]:
    project = await session.execute(
        update(ProjectModel)
        .where(
            ProjectModel.user_id == user_id,
            ProjectModel.project_id == project_id,
        )
        .values(name=project_data.name)
        .returning(ProjectModel)
    )
    await session.commit()

    if project is None:
        return

    project = project.scalar()
    return project


async def delete_project(
        user_id: int,
        project_id: int,
        session: AsyncSession,
):
    await session.execute(
        delete(ProjectModel)
        .where(
            ProjectModel.user_id == user_id,
            ProjectModel.project_id == project_id,
        )
    )
    await session.commit()

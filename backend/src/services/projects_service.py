from collections.abc import Sequence
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import DialogueModel
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

    project = await get_project_by_id(project.project_id, session)
    return project


async def get_projects(
        user_id: int,
        session: AsyncSession,
) -> Sequence[ProjectModel]:
    projects = await session.execute(
        select(ProjectModel)
        .options(
            selectinload(ProjectModel.dialogues)
            .joinedload(DialogueModel.trigger),
        )
        .where(ProjectModel.user_id == user_id)
    )
    projects = projects.unique().scalars().all()
    return projects


async def update_project(
        user_id: int,
        project_id: int,
        project_data: ProjectUpdateSchema,
        session: AsyncSession,
) -> Optional[ProjectModel]:
    project = await get_project_by_id(project_id, session)
    if project.user_id != user_id:
        return

    project.name = project_data.name
    await session.commit()
    return project


async def get_project_by_id(
        project_id: int,
        session: AsyncSession,
) -> Optional[ProjectModel]:
    project = await session.execute(
        select(ProjectModel)
        .options(
            selectinload(ProjectModel.dialogues)
            .joinedload(DialogueModel.trigger),
        )
        .where(ProjectModel.project_id == project_id)
    )
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

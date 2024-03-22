from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import ProjectModel, DialogueModel
from src.schemas.projects_schemas import ProjectReadSchema, ProjectCreateSchema, ProjectUpdateSchema


async def create_project(user_id: int, project_data: ProjectCreateSchema, session: AsyncSession):
    project = ProjectModel(**project_data.model_dump(), user_id=user_id)
    session.add(project)
    await session.commit()
    project = await get_project_by_id(project.project_id, session)
    return ProjectReadSchema.model_validate(project)


async def get_projects(user_id: int, session: AsyncSession) -> list[ProjectReadSchema]:
    projects = await session.execute(
        select(ProjectModel)
        .options(
            selectinload(ProjectModel.dialogues)
            .joinedload(DialogueModel.trigger),
        )
        .where(ProjectModel.user_id == user_id)
    )
    projects = projects.unique().scalars().all()
    return [ProjectReadSchema.model_validate(project) for project in projects]


async def get_project_by_id(project_id: int,  session: AsyncSession) -> Optional[ProjectReadSchema]:
    project = await session.execute(
        select(ProjectModel)
        .options(
            selectinload(ProjectModel.dialogues)
            .joinedload(DialogueModel.trigger),
        )
        .where(ProjectModel.project_id == project_id)
    )
    project = project.scalar()
    if project is None:
        return
    return ProjectReadSchema.model_validate(project)


async def update_project(
        project_id: int,
        project_data: ProjectUpdateSchema,
        session: AsyncSession
) -> Optional[ProjectReadSchema]:
    project = await get_project_by_id(project_id, session)
    if project is None:
        return

    project.name = project_data.name
    await session.commit()
    return project


async def delete_project(project_id: int, session: AsyncSession):
    await session.execute(
        delete(ProjectModel)
        .where(
            ProjectModel.project_id == project_id,
        )
    )
    await session.commit()

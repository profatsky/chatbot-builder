from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.models import ProjectModel, DialogueModel, BlockModel
from src.schemas.projects_schemas import (
    ProjectReadSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectToGenerateCodeReadSchema,
)


async def create_project(
        user_id: int,
        project_data: ProjectCreateSchema,
        session: AsyncSession
) -> ProjectReadSchema:
    project = ProjectModel(**project_data.model_dump(), user_id=user_id)
    session.add(project)
    await session.commit()
    project = await get_project(project.project_id, session)
    return project


async def get_projects(user_id: int, session: AsyncSession) -> list[ProjectReadSchema]:
    projects = await session.execute(
        select(ProjectModel)
        .options(
            selectinload(ProjectModel.dialogues)
            .joinedload(DialogueModel.trigger),
            selectinload(ProjectModel.plugins),
        )
        .where(ProjectModel.user_id == user_id)
    )
    projects = projects.unique().scalars().all()
    return [ProjectReadSchema.model_validate(project) for project in projects]


async def get_project(
        project_id: int,
        session: AsyncSession
) -> Optional[ProjectReadSchema]:
    project = await _get_project_model_instance(project_id, session)
    if not project:
        return
    return ProjectReadSchema.model_validate(project)


async def get_project_to_generate_code(
        project_id: int,
        session: AsyncSession
) -> Optional[ProjectToGenerateCodeReadSchema]:
    project = await session.execute(
        select(ProjectModel)
        .options(
            selectinload(ProjectModel.plugins),
            selectinload(ProjectModel.dialogues)
            .options(
                joinedload(DialogueModel.trigger),
                selectinload(DialogueModel.blocks)
                .selectin_polymorphic(BlockModel.__subclasses__()),
            )
        )
        .where(ProjectModel.project_id == project_id)
    )
    project = project.scalar()
    if project is None:
        return
    return ProjectToGenerateCodeReadSchema.model_validate(project)


async def update_project(
        project_id: int,
        project_data: ProjectUpdateSchema,
        session: AsyncSession
) -> Optional[ProjectReadSchema]:
    project = await _get_project_model_instance(project_id, session)
    if project is None:
        return

    project.name = project_data.name
    project.start_message = project_data.start_message
    project.start_keyboard_type = project_data.start_keyboard_type
    await session.commit()
    return ProjectReadSchema.model_validate(project)


async def delete_project(project_id: int, session: AsyncSession):
    await session.execute(
        delete(ProjectModel)
        .where(
            ProjectModel.project_id == project_id,
        )
    )
    await session.commit()


async def _get_project_model_instance(
        project_id: int,
        session: AsyncSession
) -> Optional[ProjectModel]:
    project = await session.execute(
        select(ProjectModel)
        .options(
            selectinload(ProjectModel.dialogues)
            .joinedload(DialogueModel.trigger),
            selectinload(ProjectModel.plugins),
        )
        .where(ProjectModel.project_id == project_id)
    )
    project = project.scalar()
    return project

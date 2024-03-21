from collections.abc import Sequence
from typing import Optional

from jinja2 import Environment, FileSystemLoader
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import DialogueModel
from src.models.projects import ProjectModel
from src.schemas.dialogues_schemas import DialogueToCodeSchema, StateSchema, StatesGroupSchema
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
    if project is None or project.user_id != user_id:
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


async def get_code(
        dialogues: list[DialogueModel],
) -> str:
    states_groups_to_code = []
    dialogues_to_code = []
    commands_values = []
    buttons_values = []

    for dialogue in dialogues:
        dialogue_to_code = DialogueToCodeSchema.model_validate(dialogue)

        if dialogue.trigger.event_type.value == 'command':
            commands_values.append(dialogue.trigger.value)
        elif dialogue.trigger.event_type.value == 'button':
            buttons_values.append(dialogue.trigger.value)

        for block in dialogue.blocks:

            if block.type == 'question_block':

                if not dialogue_to_code.has_states:
                    state = StateSchema(
                        name=f'state_from_block{block.sequence_number}'
                    )
                    states_group = StatesGroupSchema(
                        name=f'StatesGroup{len(states_groups_to_code) + 1}',
                        states=[state]
                    )
                    states_groups_to_code.append(states_group)
                    dialogue_to_code.has_states = True
                else:
                    state = StateSchema(
                        name=f'state_from_block{block.sequence_number}'
                    )
                    states_groups_to_code[-1].states.append(state)

        dialogues_to_code.append(dialogue_to_code)

    with open('src/templates/bot_template.py.j2', 'r', encoding='utf-8') as f:
        template_str = f.read()

    template = Environment(
        loader=FileSystemLoader('src/templates/'),
        trim_blocks=True,
        lstrip_blocks=True
    ).from_string(template_str)
    file_data = template.render({
        'dialogues': dialogues_to_code,
        'states_groups': states_groups_to_code,
        'commands_values': commands_values,
        'buttons_values': buttons_values,
    })
    return file_data

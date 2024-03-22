from typing import Optional

from jinja2 import Environment, FileSystemLoader, Template
from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence import projects_persistence
from src.schemas.dialogues_schemas import DialogueToCodeSchema, StateSchema, StatesGroupSchema, DialogueReadSchema
from src.schemas.projects_schemas import ProjectCreateSchema, ProjectUpdateSchema, ProjectReadSchema
from src.services import dialogues_service
from src.services.exceptions.dialogues_exceptions import NoDialoguesInProject
from src.services.exceptions.projects_exceptions import ProjectNotFound, NoPermissionForProject


async def create_project(
        user_id: int,
        project_data: ProjectCreateSchema,
        session: AsyncSession,
) -> ProjectReadSchema:
    project = await projects_persistence.create_project(user_id, project_data, session)
    return project


async def get_projects(user_id: int, session: AsyncSession) -> list[ProjectReadSchema]:
    projects = await projects_persistence.get_projects(user_id, session)
    return projects


async def get_project(user_id: int, project_id: int, session: AsyncSession):
    project = await projects_persistence.get_project(project_id, session)
    if project is None:
        raise ProjectNotFound

    if project.user_id != user_id:
        raise NoPermissionForProject

    return project


async def update_project(
        user_id: int,
        project_id: int,
        project_data: ProjectUpdateSchema,
        session: AsyncSession,
) -> Optional[ProjectReadSchema]:
    _ = await get_project(user_id, project_id, session)
    project = await projects_persistence.update_project(project_id, project_data, session)
    return project


async def delete_project(user_id: int, project_id: int, session: AsyncSession):
    _ = await get_project(user_id, project_id, session)
    await projects_persistence.delete_project(project_id, session)


async def get_bot_code(
        user_id: int,
        project_id: int,
        session: AsyncSession,
) -> str:
    _ = await get_project(user_id, project_id, session)

    dialogues = await dialogues_service.get_dialogues_with_blocks(project_id, session)
    if not dialogues:
        raise NoDialoguesInProject

    code = _generate_bot_code(dialogues)
    return code


def _generate_bot_code(dialogues: list[DialogueReadSchema]) -> str:
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

    template = _get_bot_template()
    bot_code = template.render({
        'dialogues': dialogues_to_code,
        'states_groups': states_groups_to_code,
        'commands_values': commands_values,
        'buttons_values': buttons_values,
    })
    return bot_code


def _get_bot_template() -> Template:
    with open('src/templates/bot_template.py.j2', 'r', encoding='utf-8') as f:
        template_str = f.read()

    env = Environment(
        loader=FileSystemLoader('src/templates/'),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.from_string(template_str)
    return template

from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence import dialogues_persistence
from src.schemas.dialogues_schemas import (
    DialogueCreateSchema,
    DialogueReadSchema,
    TriggerUpdateSchema,
)
from src.services import projects_service
from src.services.exceptions.dialogues_exceptions import DialogueNotFound


async def check_access_and_create_dialogue(
        user_id: int,
        project_id: int,
        dialogue_data: DialogueCreateSchema,
        session: AsyncSession,
) -> DialogueReadSchema:
    _ = await projects_service.check_access_and_get_project(user_id, project_id, session)
    dialogue = await dialogues_persistence.create_dialogue(project_id, dialogue_data, session)
    return dialogue


async def check_access_and_update_dialogue_trigger(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        trigger: TriggerUpdateSchema,
        session: AsyncSession,
) -> DialogueReadSchema:
    _ = await projects_service.check_access_and_get_project(user_id, project_id, session)

    dialogue = await dialogues_persistence.update_dialogue_trigger(dialogue_id, trigger, session)
    if dialogue is None:
        raise DialogueNotFound

    return dialogue


async def check_access_and_get_dialogue(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        session: AsyncSession,
) -> DialogueReadSchema:
    project = await projects_service.check_access_and_get_project(user_id, project_id, session)

    dialogue_with_specified_id = None
    for dialogue in project.dialogues:
        if dialogue.dialogue_id == dialogue_id:
            dialogue_with_specified_id = dialogue
            break

    if dialogue_with_specified_id is None:
        raise DialogueNotFound

    return dialogue_with_specified_id


async def check_access_and_delete_dialogue(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        session: AsyncSession
):
    _ = await check_access_and_get_dialogue(user_id, project_id, dialogue_id, session)
    await dialogues_persistence.delete_dialogue(dialogue_id, session)

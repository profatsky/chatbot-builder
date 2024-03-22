from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence import dialogues_persistence
from src.schemas.blocks_schemas import UnionBlockCreateSchema, UnionBlockReadSchema
from src.schemas.dialogues_schemas import (
    DialogueCreateSchema,
    DialogueWithoutBlocksReadSchema,
    DialogueWithBlocksReadSchema,
    TriggerUpdateSchema,
)
from src.schemas.projects_schemas import ProjectReadSchema
from src.services import projects_service
from src.services.exceptions.dialogues_exceptions import DialogueNotFound, RepeatingSequenceNumbersForBlocks


async def check_access_and_create_dialogue(
        user_id: int,
        project_id: int,
        dialogue_data: DialogueCreateSchema,
        session: AsyncSession,
) -> DialogueWithoutBlocksReadSchema:
    _ = await projects_service.check_access_and_get_project(user_id, project_id, session)
    dialogue = await _create_dialogue(project_id, dialogue_data, session)
    return dialogue


async def _create_dialogue(
        project_id: int,
        dialogue_data: DialogueCreateSchema,
        session: AsyncSession,
) -> DialogueWithoutBlocksReadSchema:
    dialogue = await dialogues_persistence.create_dialogue(project_id, dialogue_data, session)
    return dialogue


async def check_access_and_update_dialogue_trigger(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        trigger: TriggerUpdateSchema,
        session: AsyncSession,
) -> DialogueWithoutBlocksReadSchema:
    _ = await projects_service.check_access_and_get_project(user_id, project_id, session)

    dialogue = await dialogues_persistence.update_dialogue_trigger(dialogue_id, trigger, session)
    if dialogue is None:
        raise DialogueNotFound

    return dialogue


async def get_dialogues_with_blocks(project_id: int, session: AsyncSession) -> list[DialogueWithBlocksReadSchema]:
    dialogues = await dialogues_persistence.get_dialogues_with_blocks(project_id, session)
    _sort_blocks_in_dialogue_by_sequence_number(dialogues)
    return dialogues


def _sort_blocks_in_dialogue_by_sequence_number(dialogues: list[DialogueWithBlocksReadSchema]):
    for dialogue in dialogues:
        dialogue.blocks.sort(key=lambda x: x.sequence_number)


async def check_access_and_update_blocks_in_dialogue(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        blocks: list[UnionBlockCreateSchema],
        session: AsyncSession,
) -> list[UnionBlockReadSchema]:
    project = await projects_service.check_access_and_get_project(user_id, project_id, session)
    if not _project_contain_dialogue_with_specified_id(project, dialogue_id):
        raise DialogueNotFound

    if not _all_sequence_numbers_are_unique(blocks):
        raise RepeatingSequenceNumbersForBlocks

    blocks = await _update_blocks_in_dialogue(dialogue_id, blocks, session)
    return blocks


async def _update_blocks_in_dialogue(
        dialogue_id: int,
        blocks: list[UnionBlockCreateSchema],
        session: AsyncSession,
) -> list[UnionBlockReadSchema]:
    blocks = await dialogues_persistence.update_blocks_in_dialogue(dialogue_id, blocks, session)
    return blocks


def _all_sequence_numbers_are_unique(blocks: list[UnionBlockCreateSchema]) -> bool:
    sequence_numbers = [block.sequence_number for block in blocks]
    return len(sequence_numbers) == len(set(sequence_numbers))


async def check_access_and_get_blocks_in_dialogue(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        session: AsyncSession,
) -> list[UnionBlockReadSchema]:
    project = await projects_service.check_access_and_get_project(user_id, project_id, session)
    if not _project_contain_dialogue_with_specified_id(project, dialogue_id):
        raise DialogueNotFound

    blocks = await _get_blocks_in_dialogue(dialogue_id, session)
    return blocks


def _project_contain_dialogue_with_specified_id(project: ProjectReadSchema, dialogue_id: int) -> bool:
    project_dialogue_ids = [dialogue.dialogue_id for dialogue in project.dialogues]
    return dialogue_id in project_dialogue_ids


async def _get_blocks_in_dialogue(dialogue_id: int, session: AsyncSession) -> list[UnionBlockReadSchema]:
    blocks = await dialogues_persistence.get_blocks_in_dialogue(dialogue_id, session)
    return blocks


async def check_access_and_delete_dialogue(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        session: AsyncSession
):
    project = await projects_service.check_access_and_get_project(user_id, project_id, session)
    if not _project_contain_dialogue_with_specified_id(project, dialogue_id):
        raise DialogueNotFound

    await dialogues_persistence.delete_dialogue(dialogue_id, session)

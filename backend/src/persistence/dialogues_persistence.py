from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import DialogueModel, TriggerModel, BlockModel
from src.schemas.blocks_schemas import UnionBlockCreateSchema, UnionBlockReadSchema
from src.schemas.dialogues_schemas import (
    DialogueCreateSchema,
    DialogueReadSchema,
    TriggerUpdateSchema,
)
from src.utils import blocks_utils


async def create_dialogue(
        project_id: int,
        dialogue_data: DialogueCreateSchema,
        session: AsyncSession,
) -> DialogueReadSchema:
    trigger = TriggerModel(**dialogue_data.trigger.model_dump())
    dialogue = DialogueModel(trigger=trigger, project_id=project_id)
    session.add(dialogue)
    await session.commit()
    return DialogueReadSchema.model_validate(dialogue)


async def update_dialogue_trigger(
        dialogue_id: int,
        trigger: TriggerUpdateSchema,
        session: AsyncSession,
) -> Optional[DialogueReadSchema]:
    dialogue = await _get_dialogue(dialogue_id, session)
    if dialogue is None:
        return

    dialogue.trigger.event_type = trigger.event_type
    dialogue.trigger.value = trigger.value
    await session.commit()
    return DialogueReadSchema.model_validate(dialogue)


async def _get_dialogue(dialogue_id: int, session: AsyncSession) -> Optional[DialogueModel]:
    dialogue = await session.execute(
        select(DialogueModel)
        .options(
            joinedload(DialogueModel.trigger),
        )
        .where(DialogueModel.dialogue_id == dialogue_id)
    )
    dialogue = dialogue.scalar()
    return dialogue


async def delete_dialogue(dialogue_id: int, session: AsyncSession):
    await session.execute(
        delete(DialogueModel)
        .where(DialogueModel.dialogue_id == dialogue_id)
    )
    await session.commit()

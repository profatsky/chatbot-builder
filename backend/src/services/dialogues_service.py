from sqlalchemy.ext.asyncio import AsyncSession

from src.models import DialogueModel, TriggerModel
from src.schemas.dialogue_schemas import DialogueCreateSchema


async def create_dialogue(
        project_id: int,
        dialogue_data: DialogueCreateSchema,
        session: AsyncSession,
) -> DialogueModel:
    trigger = TriggerModel(**dialogue_data.trigger.model_dump())
    dialogue = DialogueModel(trigger=trigger, project_id=project_id)
    session.add(dialogue)
    await session.commit()
    return dialogue

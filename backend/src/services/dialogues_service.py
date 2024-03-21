from sqlalchemy import select, delete
from sqlalchemy.orm import selectin_polymorphic, selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import DialogueModel, TriggerModel, BlockModel
from src.schemas.blocks_schemas import UnionBlockCreateSchema
from src.schemas.dialogues_schemas import DialogueCreateSchema
from src.utils import blocks_utils


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


async def get_dialogues(
        project_id: int,
        session: AsyncSession,
) -> list[DialogueModel]:
    dialogues = await session.execute(
        select(DialogueModel)
        .options(
            joinedload(DialogueModel.trigger),
            selectinload(DialogueModel.blocks)
            .selectin_polymorphic(BlockModel.__subclasses__())
        )
        .where(DialogueModel.project_id == project_id)
        .order_by(DialogueModel.created_at)
    )
    dialogues = dialogues.unique().scalars().all()

    for dialogue in dialogues:
        dialogue.blocks.sort(key=lambda x: x.sequence_number)

    return dialogues


async def update_blocks_in_dialogue(
        dialogue_id: int,
        blocks: list[UnionBlockCreateSchema],
        session: AsyncSession,
):
    await session.execute(
        delete(BlockModel)
        .where(BlockModel.dialogue_id == dialogue_id)
    )

    for block_schema in blocks:
        block_model = blocks_utils.get_block_model_by_type(block_schema.type)
        block = block_model(**block_schema.model_dump(), dialogue_id=dialogue_id)
        session.add(block)

    await session.commit()


async def get_blocks_in_dialogue(
        dialogue_id: int,
        session: AsyncSession,
) -> list[BlockModel]:
    blocks = await session.execute(
        select(BlockModel)
        .options(
            selectin_polymorphic(BlockModel, BlockModel.__subclasses__()),
        )
        .where(BlockModel.dialogue_id == dialogue_id)
        .order_by(BlockModel.sequence_number)
    )
    blocks = blocks.unique().scalars().all()
    return blocks

from sqlalchemy import select, delete
from sqlalchemy.orm import selectin_polymorphic, selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import DialogueModel, TriggerModel, BlockModel
from src.schemas.blocks_schemas import UnionBlockCreateSchema, UnionBlockReadSchema
from src.schemas.dialogues_schemas import DialogueCreateSchema, DialogueReadSchema, DialogueReadSchemaWithBlocks
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


async def get_dialogues_with_blocks(project_id: int, session: AsyncSession) -> list[DialogueReadSchemaWithBlocks]:
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
    return [DialogueReadSchemaWithBlocks.model_validate(dialogue) for dialogue in dialogues]


async def update_blocks_in_dialogue(
        dialogue_id: int,
        blocks: list[UnionBlockCreateSchema],
        session: AsyncSession,
) -> list[UnionBlockReadSchema]:
    await session.execute(
        delete(BlockModel)
        .where(BlockModel.dialogue_id == dialogue_id)
    )

    new_blocks = []
    for block_schema in blocks:
        block_model = blocks_utils.get_block_model_by_type(block_schema.type)
        block = block_model(**block_schema.model_dump(), dialogue_id=dialogue_id)
        new_blocks.append(block)
        session.add(block)

    await session.commit()

    return [blocks_utils.validate_block_from_db(block) for block in new_blocks]


async def get_blocks_in_dialogue(dialogue_id: int, session: AsyncSession) -> list[UnionBlockReadSchema]:
    blocks = await session.execute(
        select(BlockModel)
        .options(
            selectin_polymorphic(BlockModel, BlockModel.__subclasses__()),
        )
        .where(BlockModel.dialogue_id == dialogue_id)
        .order_by(BlockModel.sequence_number)
    )
    blocks = blocks.unique().scalars().all()
    return [blocks_utils.validate_block_from_db(block) for block in blocks]

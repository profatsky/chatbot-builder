from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectin_polymorphic

from src.models import BlockModel
from src.schemas.blocks_schemas import UnionBlockCreateSchema, UnionBlockReadSchema, UnionBlockUpdateSchema
from src.utils import blocks_utils
from src.utils.blocks_utils import UnionBlockModel


async def create_block(
        dialogue_id: int,
        block_data: UnionBlockCreateSchema,
        session: AsyncSession,
) -> UnionBlockReadSchema:
    blocks = await get_blocks(dialogue_id, session)
    blocks_number = len(blocks)

    block_model = blocks_utils.get_block_model_by_type(block_data.type)
    block = block_model(**block_data.model_dump(), dialogue_id=dialogue_id, sequence_number=blocks_number + 1)
    session.add(block)
    await session.commit()

    return blocks_utils.validate_block_from_db(block)


async def get_blocks(dialogue_id: int, session: AsyncSession) -> list[UnionBlockReadSchema]:
    blocks = await _get_blocks(dialogue_id, session)
    return [blocks_utils.validate_block_from_db(block) for block in blocks]


async def _get_blocks(dialogue_id: int, session: AsyncSession) -> list[UnionBlockModel]:
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


# async def get_block(block_id: int, session: AsyncSession) -> Optional[UnionBlockReadSchema]:
#     block = await _get_block(block_id, session)
#     return blocks_utils.validate_block_from_db(block)


async def _get_block(block_id: int, session: AsyncSession) -> Optional[UnionBlockModel]:
    block = await session.execute(
        select(BlockModel)
        .where(BlockModel.block_id == block_id)
    )
    block = block.scalar()
    return block


async def update_block(
        dialogue_id: int,
        block_id: int,
        block_data: UnionBlockUpdateSchema,
        session: AsyncSession,
) -> Optional[UnionBlockReadSchema]:
    block = await _get_block(block_id, session)

    for key, value in block_data.model_dump().items():
        setattr(block, key, value)

    await _update_blocks_sequence_numbers_without_commit(dialogue_id, session)
    await session.commit()

    return blocks_utils.validate_block_from_db(block)


async def _update_blocks_sequence_numbers_without_commit(
        dialogue_id: int,
        session: AsyncSession,
) -> Optional[UnionBlockReadSchema]:
    blocks = await _get_blocks(dialogue_id, session)
    counter = 1
    for block in sorted(blocks, key=lambda x: x.sequence_number):
        block.sequence_number = counter
        counter += 1

    return [blocks_utils.validate_block_from_db(block) for block in blocks]


async def delete_block(
        dialogue_id: int,
        block_id: int,
        session: AsyncSession,
) -> Optional[UnionBlockReadSchema]:
    await session.execute(
        delete(BlockModel)
        .where(BlockModel.block_id == block_id)
    )
    await _update_blocks_sequence_numbers_without_commit(dialogue_id, session)
    await session.commit()

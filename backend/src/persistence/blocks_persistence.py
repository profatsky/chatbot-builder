from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectin_polymorphic

from src.models import BlockModel
from src.schemas.blocks_schemas import UnionBlockCreateSchema, UnionBlockReadSchema, UnionBlockUpdateSchema
from src.utils import blocks_utils


async def create_block(
        dialogue_id: int,
        block_data: UnionBlockCreateSchema,
        session: AsyncSession,
) -> UnionBlockReadSchema:
    block_model = blocks_utils.get_block_model_by_type(block_data.type)
    block = block_model(**block_data.model_dump(), dialogue_id=dialogue_id)
    session.add(block)
    await session.commit()
    return blocks_utils.validate_block_from_db(block)


async def get_blocks(dialogue_id: int, session: AsyncSession) -> list[UnionBlockReadSchema]:
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


async def _get_block(block_id: int, session: AsyncSession) -> Optional[BlockModel]:
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
    await delete_block(block_id, session)
    block = await create_block(dialogue_id, block_data, session)
    return block


async def delete_block(block_id: int, session: AsyncSession):
    await session.execute(
        delete(BlockModel)
        .where(BlockModel.block_id == block_id)
    )
    await session.commit()

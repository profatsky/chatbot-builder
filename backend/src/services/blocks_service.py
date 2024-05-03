from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence import blocks_persistence
from src.schemas.blocks_schemas import UnionBlockCreateSchema, UnionBlockReadSchema, UnionBlockUpdateSchema
from src.services import dialogues_service
from src.services.exceptions.blocks_exceptions import BlockNotFound, RepeatingBlockSequenceNumber


async def check_access_and_create_block(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        block_data: UnionBlockCreateSchema,
        session: AsyncSession,
) -> UnionBlockReadSchema:
    blocks = await check_access_and_get_blocks(user_id, project_id, dialogue_id, session)

    for block in blocks:
        if block.sequence_number == block_data.sequence_number:
            raise RepeatingBlockSequenceNumber

    block = await blocks_persistence.create_block(dialogue_id, block_data, session)
    return block


async def check_access_and_get_blocks(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        session: AsyncSession,
) -> list[UnionBlockReadSchema]:
    _ = await dialogues_service.check_access_and_get_dialogue(user_id, project_id, dialogue_id, session)

    blocks = await blocks_persistence.get_blocks(dialogue_id, session)
    blocks.sort(key=lambda x: x.sequence_number)
    return blocks


async def check_access_and_update_block(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        block_id: int,
        block_data: UnionBlockUpdateSchema,
        session: AsyncSession,
) -> UnionBlockReadSchema:
    blocks = await check_access_and_get_blocks(user_id, project_id, dialogue_id, session)

    block_with_specified_id = None
    for block in blocks:
        if block.block_id == block_id:
            block_with_specified_id = block
            break

    if block_with_specified_id is None:
        raise BlockNotFound

    if block_with_specified_id.sequence_number != block_data.sequence_number:
        raise RepeatingBlockSequenceNumber

    block = await blocks_persistence.update_block(dialogue_id, block_id, block_data, session)
    return block


async def check_access_and_delete_block(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        block_id: int,
        session: AsyncSession,
) -> UnionBlockReadSchema:
    blocks = await check_access_and_get_blocks(user_id, project_id, dialogue_id, session)

    block_with_specified_id = [block for block in blocks if block.block_id == block_id]
    if not block_with_specified_id:
        raise BlockNotFound

    await blocks_persistence.delete_block(block_id, session)
    await blocks_persistence.update_blocks_sequence_numbers(dialogue_id, session)

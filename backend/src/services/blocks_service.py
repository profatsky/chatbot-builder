import os.path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.enums import BlockType
from src.persistence import blocks_persistence
from src.schemas.blocks_schemas import UnionBlockCreateSchema, UnionBlockReadSchema, UnionBlockUpdateSchema, \
    ImageBlockReadSchema
from src.services import dialogues_service
from src.services.exceptions.blocks_exceptions import BlockNotFound, RepeatingBlockSequenceNumber, InvalidBlockType


async def check_access_and_create_block(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        block_data: UnionBlockCreateSchema,
        session: AsyncSession,
) -> UnionBlockReadSchema:
    _ = await dialogues_service.check_access_and_get_dialogue(user_id, project_id, dialogue_id, session)
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


async def check_access_and_upload_image_for_image_block(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        block_id: int,
        image: UploadFile,
        session: AsyncSession,
) -> ImageBlockReadSchema:
    block_read = await _check_access_and_get_block(user_id, project_id, dialogue_id, block_id, session)
    if block_read.type != BlockType.IMAGE_BLOCK.value:
        raise InvalidBlockType

    if block_read.image_path:
        full_image_path = os.path.join('src', 'media', block_read.image_path)
        if os.path.exists(full_image_path):
            os.remove(full_image_path)

    image_path = f'src/media/users/{user_id}/projects/{project_id}/dialogues/{dialogue_id}/{image.filename}'
    if not os.path.exists(os.path.dirname(image_path)):
        os.makedirs(os.path.dirname(image_path))

    with open(image_path, 'wb+') as buffer:
        buffer.write(image.file.read())

    block_update = ImageBlockReadSchema(**{
        field_name: getattr(block_read, field_name)
        for field_name in ImageBlockReadSchema.__fields__
    })
    block_update.image_path = image_path.replace('src/media/', '')

    block = await check_access_and_update_block(user_id, project_id, dialogue_id, block_id, block_update, session)
    return block


async def check_access_and_update_block(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        block_id: int,
        block_data: UnionBlockUpdateSchema,
        session: AsyncSession,
) -> UnionBlockReadSchema:
    _ = await _check_access_and_get_block(user_id, project_id, dialogue_id, block_id, session)
    block = await blocks_persistence.update_block(dialogue_id, block_id, block_data, session)
    return block


async def check_access_and_delete_block(
        user_id: int,
        project_id: int,
        dialogue_id: int,
        block_id: int,
        session: AsyncSession,
) -> UnionBlockReadSchema:
    block = await _check_access_and_get_block(user_id, project_id, dialogue_id, block_id, session)
    if block.type == BlockType.IMAGE_BLOCK.value and block.image_path:
        full_image_path = os.path.join('src', 'media', block.image_path)
        if os.path.exists(full_image_path):
            os.remove(full_image_path)

    await blocks_persistence.delete_block(dialogue_id, block_id, session)


async def _check_access_and_get_block(
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

    return block_with_specified_id[0]

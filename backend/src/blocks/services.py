import os

from fastapi import UploadFile

from src.blocks.dependencies.repositories_dependencies import BlockRepositoryDI
from src.dialogues.dependencies.services_dependencies import DialogueServiceDI
from src.enums import BlockType
from src.blocks.schemas import (
    UnionBlockCreateSchema,
    UnionBlockReadSchema,
    UnionBlockUpdateSchema,
    ImageBlockReadSchema,
)
from src.blocks.exceptions.services_exceptions import BlockNotFoundError, InvalidBlockTypeError


class BlockService:
    def __init__(
            self,
            block_repository: BlockRepositoryDI,
            dialogue_service: DialogueServiceDI,
    ):
        self._block_repository = block_repository
        self._dialogue_service = dialogue_service

    async def check_access_and_create_block(
            self,
            user_id: int,
            project_id: int,
            dialogue_id: int,
            block_data: UnionBlockCreateSchema,
    ) -> UnionBlockReadSchema:
        _ = await self._dialogue_service.get_dialogue(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
        )
        block = await self._block_repository.create_block(
            dialogue_id=dialogue_id,
            block_data=block_data,
        )
        return block

    async def check_access_and_get_blocks(
            self,
            user_id: int,
            project_id: int,
            dialogue_id: int,
    ) -> list[UnionBlockReadSchema]:
        _ = await self._dialogue_service.get_dialogue(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
        )

        blocks = await self._block_repository.get_blocks(dialogue_id)
        blocks.sort(key=lambda x: x.sequence_number)
        return blocks

    async def check_access_and_upload_image_for_image_block(
            self,
            user_id: int,
            project_id: int,
            dialogue_id: int,
            block_id: int,
            image: UploadFile,
    ) -> ImageBlockReadSchema:
        block_read = await self._check_access_and_get_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
        )
        if block_read.type != BlockType.IMAGE_BLOCK.value:
            raise InvalidBlockTypeError

        if block_read.image_path:
            full_image_path = os.path.join('src', 'media', block_read.image_path)
            if os.path.exists(full_image_path):
                os.remove(full_image_path)

        # TODO: use os.path.join
        image_path = f'src/media/users/{user_id}/projects/{project_id}/dialogues/{dialogue_id}/{image.filename}'
        if not os.path.exists(os.path.dirname(image_path)):
            os.makedirs(os.path.dirname(image_path))

        with open(image_path, 'wb+') as buffer:
            buffer.write(image.file.read())

        block_update = ImageBlockReadSchema(**{
            field_name: getattr(block_read, field_name)
            for field_name in ImageBlockReadSchema.__fields__
        })
        # TODO: use os.path.join
        block_update.image_path = image_path.replace('src/media/', '')

        block = await self.check_access_and_update_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
            block_data=block_update,
        )
        return block

    async def check_access_and_update_block(
            self,
            user_id: int,
            project_id: int,
            dialogue_id: int,
            block_id: int,
            block_data: UnionBlockUpdateSchema,
    ) -> UnionBlockReadSchema:
        _ = await self._check_access_and_get_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
        )
        block = await self._block_repository.update_block(
            dialogue_id=dialogue_id,
            block_id=block_id,
            block_data=block_data,
        )
        return block

    async def check_access_and_delete_block(
            self,
            user_id: int,
            project_id: int,
            dialogue_id: int,
            block_id: int,
    ) -> UnionBlockReadSchema:
        block = await self._check_access_and_get_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
        )
        if block.type == BlockType.IMAGE_BLOCK.value and block.image_path:
            full_image_path = os.path.join('src', 'media', block.image_path)
            if os.path.exists(full_image_path):
                os.remove(full_image_path)

        await self._block_repository.delete_block(
            dialogue_id=dialogue_id,
            block_id=block_id,
        )

    async def _check_access_and_get_block(
            self,
            user_id: int,
            project_id: int,
            dialogue_id: int,
            block_id: int,
    ) -> UnionBlockReadSchema:
        blocks = await self.check_access_and_get_blocks(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
        )

        block_with_specified_id = [block for block in blocks if block.block_id == block_id]
        if not block_with_specified_id:
            raise BlockNotFoundError

        return block_with_specified_id[0]

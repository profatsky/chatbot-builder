from typing import Annotated

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status, HTTPException, UploadFile
from fastapi.params import Depends

from src.blocks.dependencies.services_dependencies import BlockServiceDI
from src.core.auth import auth_dep
from src.blocks.schemas import UnionBlockCreateSchema, UnionBlockReadSchema, UnionBlockUpdateSchema
from src.projects import exceptions as projects_exceptions
from src.dialogues import exceptions as dialogues_exceptions
from src.blocks import exceptions as blocks_exceptions

router = APIRouter(
    prefix='/projects/{project_id}/dialogues/{dialogue_id}/blocks',
    tags=['blocks'],
)


@router.post('', response_model=UnionBlockReadSchema)
async def create_block(
        project_id: int,
        dialogue_id: int,
        block: UnionBlockCreateSchema,
        auth_jwt: Annotated[AuthJWT, Depends(auth_dep)],
        block_service: BlockServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        block = await block_service.check_access_and_create_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_data=block,
        )
    except projects_exceptions.ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project does not exist',
        )
    except projects_exceptions.NoPermissionForProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )
    except dialogues_exceptions.DialogueNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dialogue does not exist',
        )
    except blocks_exceptions.RepeatingBlockSequenceNumber:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Repeating sequence numbers for blocks in the dialogue',
        )
    return block


@router.get('', response_model=list[UnionBlockReadSchema])
async def get_blocks(
        project_id: int,
        dialogue_id: int,
        auth_jwt: Annotated[AuthJWT, Depends(auth_dep)],
        block_service: BlockServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        blocks = await block_service.check_access_and_get_blocks(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
        )
    except projects_exceptions.ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project does not exist',
        )
    except projects_exceptions.NoPermissionForProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )
    except dialogues_exceptions.DialogueNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dialogue does not exist',
        )
    return blocks


@router.put('/{block_id}', response_model=UnionBlockReadSchema)
async def update_block(
        project_id: int,
        dialogue_id: int,
        block_id: int,
        block: UnionBlockUpdateSchema,
        auth_jwt: Annotated[AuthJWT, Depends(auth_dep)],
        block_service: BlockServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        block = await block_service.check_access_and_update_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
            block_data=block,
        )
    except projects_exceptions.ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project does not exist',
        )
    except projects_exceptions.NoPermissionForProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )
    except dialogues_exceptions.DialogueNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dialogue does not exist',
        )
    except blocks_exceptions.BlockNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Block does not exits',
        )
    except blocks_exceptions.RepeatingBlockSequenceNumber:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Repeating sequence numbers for blocks in the dialogue',
        )
    return block


@router.post('/{block_id}/upload-image', response_model=UnionBlockReadSchema)
async def upload_image_for_image_block(
        project_id: int,
        dialogue_id: int,
        block_id: int,
        image: UploadFile,
        auth_jwt: Annotated[AuthJWT, Depends(auth_dep)],
        block_service: BlockServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        block = await block_service.check_access_and_upload_image_for_image_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
            image=image,
        )
    except projects_exceptions.ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project does not exist',
        )
    except projects_exceptions.NoPermissionForProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )
    except dialogues_exceptions.DialogueNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dialogue does not exist',
        )
    except blocks_exceptions.BlockNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Block does not exits',
        )
    except blocks_exceptions.InvalidBlockType:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid block type'
        )
    return block


@router.delete('/{block_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_block(
        project_id: int,
        dialogue_id: int,
        block_id: int,
        auth_jwt: Annotated[AuthJWT, Depends(auth_dep)],
        block_service: BlockServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await block_service.check_access_and_delete_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
        )
    except projects_exceptions.ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project does not exist',
        )
    except projects_exceptions.NoPermissionForProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )
    except dialogues_exceptions.DialogueNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dialogue does not exist',
        )
    except blocks_exceptions.BlockNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Block does not exits',
        )
    return {'detail': 'Block was successfully deleted'}

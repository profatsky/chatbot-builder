from typing import Annotated

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status, HTTPException, UploadFile
from fastapi.params import Depends

from src.blocks.dependencies.services_dependencies import BlockServiceDI
from src.blocks.exceptions import RepeatingBlockSequenceNumberError, BlockNotFoundError, InvalidBlockTypeError
from src.core.auth import auth_dep
from src.blocks.schemas import UnionBlockCreateSchema, UnionBlockReadSchema, UnionBlockUpdateSchema
from src.dialogues.exceptions.http_exceptions import DialogueNotFoundHTTPException
from src.dialogues.exceptions.services_exceptions import DialogueNotFoundError
from src.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException, NoPermissionForProjectHTTPException

router = APIRouter(
    prefix='/projects/{project_id}/dialogues/{dialogue_id}/blocks',
    tags=['Blocks'],
)


@router.post(
    '',
    response_model=UnionBlockReadSchema,
    status_code=status.HTTP_201_CREATED,
)
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
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException

    except RepeatingBlockSequenceNumberError:
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
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException

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
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException

    except BlockNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Block does not exits',
        )
    except RepeatingBlockSequenceNumberError:
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
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException

    except BlockNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Block does not exits',
        )
    except InvalidBlockTypeError:
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
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException

    except BlockNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Block does not exits',
        )
    return {'detail': 'Block was successfully deleted'}

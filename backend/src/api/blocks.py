from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.blocks_schemas import UnionBlockCreateSchema, UnionBlockReadSchema, UnionBlockUpdateSchema
from src.services import blocks_service
from src.services.exceptions import projects_exceptions, dialogues_exceptions, blocks_exceptions

router = APIRouter(
    prefix='/projects/{project_id}/dialogues/{dialogue_id}/blocks',
    tags=['blocks'],
)


@router.post('', response_model=UnionBlockReadSchema)
async def create_block(
        project_id: int,
        dialogue_id: int,
        block: UnionBlockCreateSchema,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep)
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        block = await blocks_service.check_access_and_create_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_data=block,
            session=session
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
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep)
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        blocks = await blocks_service.check_access_and_get_blocks(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            session=session
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
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
) -> UnionBlockReadSchema:
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        block = await blocks_service.check_access_and_update_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
            block_data=block,
            session=session,
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


@router.delete('/{block_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_block(
        project_id: int,
        dialogue_id: int,
        block_id: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await blocks_service.check_access_and_delete_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
            session=session
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
    return {'detail': 'Блок успешно удален'}

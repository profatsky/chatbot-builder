from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.blocks_schemas import UnionBlockCreateSchema, UnionBlockReadSchema
from src.schemas.dialogues_schemas import DialogueCreateSchema, DialogueWithoutBlocksReadSchema, TriggerUpdateSchema
from src.services import dialogues_service
from src.services.exceptions import projects_exceptions, dialogues_exceptions

router = APIRouter(
    prefix='/projects/{project_id}/dialogues',
    tags=['dialogues'],
)


@router.post('', response_model=DialogueWithoutBlocksReadSchema, status_code=status.HTTP_201_CREATED)
async def create_dialogue(
        project_id: int,
        dialogue_data: DialogueCreateSchema,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        dialogue = await dialogues_service.check_access_and_create_dialogue(
            user_id=user_id,
            project_id=project_id,
            dialogue_data=dialogue_data,
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
    return dialogue


@router.put('/{dialogue_id}', response_model=DialogueWithoutBlocksReadSchema)
async def update_dialogue_trigger(
        project_id: int,
        dialogue_id: int,
        trigger: TriggerUpdateSchema,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        dialogue = await dialogues_service.check_access_and_update_dialogue_trigger(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            trigger=trigger,
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
    return dialogue


@router.get('/{dialogue_id}', response_model=list[UnionBlockReadSchema])
async def get_blocks_in_dialogue(
        project_id: int,
        dialogue_id: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        blocks = await dialogues_service.check_access_and_get_blocks_in_dialogue(
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


@router.patch('/{dialogue_id}', response_model=list[UnionBlockReadSchema])
async def update_blocks_in_dialogue(
        project_id: int,
        dialogue_id: int,
        blocks: list[UnionBlockCreateSchema],
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        blocks = await dialogues_service.check_access_and_update_blocks_in_dialogue(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            blocks=blocks,
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
    except dialogues_exceptions.RepeatingSequenceNumbersForBlocks:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Repeating sequence numbers for blocks in the dialog',
        )
    return blocks


@router.delete('/{dialogue_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_dialogue(
        project_id: int,
        dialogue_id: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await dialogues_service.check_access_and_delete_dialogue(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
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
    return {'message': 'Project was successfully deleted'}

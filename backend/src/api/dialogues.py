from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.blocks_schemas import UnionBlockCreateSchema, UnionBlockReadSchema
from src.schemas.dialogues_schemas import DialogueCreateSchema, DialogueReadSchema
from src.services import dialogues_service, projects_service

router = APIRouter(
    prefix='/projects/{project_id}/dialogues',
    tags=['dialogues'],
)


@router.post('', response_model=DialogueReadSchema, status_code=status.HTTP_201_CREATED)
async def create_dialogue(
        project_id: int,
        dialogue_data: DialogueCreateSchema,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    project = await projects_service.get_project_by_id(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project does not exist',
        )

    if project.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\'t have permission'
        )

    dialogue = await dialogues_service.create_dialogue(
        project_id=project_id,
        dialogue_data=dialogue_data,
        session=session
    )
    return dialogue


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

    project = await projects_service.get_project_by_id(project_id, session)

    if project.user_id != user_id or dialogue_id not in [dialogue.dialogue_id for dialogue in project.dialogues]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\'t have permission'
        )

    await dialogues_service.update_blocks_in_dialogue(
        dialogue_id=dialogue_id,
        blocks=blocks,
        session=session
    )
    blocks = await dialogues_service.get_blocks_in_dialogue(dialogue_id, session)
    return blocks


@router.get('/{dialogue_id}', response_model=list[UnionBlockReadSchema])
async def get_dialogue(
        project_id: int,
        dialogue_id: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    project = await projects_service.get_project_by_id(project_id, session)
    if project.user_id != user_id or dialogue_id not in [dialogue.dialogue_id for dialogue in project.dialogues]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\'t have permission'
        )

    blocks = await dialogues_service.get_blocks_in_dialogue(dialogue_id, session)
    return blocks

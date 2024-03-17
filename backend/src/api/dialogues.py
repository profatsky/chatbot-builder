from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.dialogue_schemas import DialogueCreateSchema, DialogueReadSchema
from src.services import dialogues_service

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

    dialogue = await dialogues_service.create_dialogue(
        project_id=project_id,
        dialogue_data=dialogue_data,
        session=session
    )
    return dialogue

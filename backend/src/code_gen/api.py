from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.dialogues.schemas import DialogueWithBlocksReadSchema
from src.projects import exceptions as projects_exceptions
from src.dialogues import exceptions as dialogues_exceptions
from src.code_gen import services as code_generation_service

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
)


@router.get('/{project_id}/code', response_model=list[DialogueWithBlocksReadSchema])
async def get_bot_code(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        zipped_bot = await code_generation_service.get_bot_code_in_zip(user_id, project_id, session)
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
    except dialogues_exceptions.NoDialoguesInProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No dialogues in the project'
        )

    return StreamingResponse(
        zipped_bot,
        media_type='application/zip',
        headers={'Content-Disposition': 'attachment; filename=bot.zip'}
    )

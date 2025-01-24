from typing import Annotated

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import StreamingResponse

from src.code_gen.dependencies.services_dependencies import CodeGenServiceDI
from src.core.auth import auth_dep
from src.dialogues.exceptions.http_exceptions import NoDialoguesInProjectHTTPException
from src.dialogues.exceptions.services_exceptions import NoDialoguesInProjectError
from src.dialogues.schemas import DialogueWithBlocksReadSchema
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException, NoPermissionForProjectHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError

router = APIRouter(
    prefix='/projects',
    tags=['Projects'],
)


@router.get('/{project_id}/code', response_model=list[DialogueWithBlocksReadSchema])
async def get_bot_code(
        project_id: int,
        auth_jwt: Annotated[AuthJWT, Depends(auth_dep)],
        code_gen_service: CodeGenServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        zipped_bot = await code_gen_service.get_bot_code_in_zip(
            user_id=user_id,
            project_id=project_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except NoDialoguesInProjectError:
        raise NoDialoguesInProjectHTTPException

    return StreamingResponse(
        content=zipped_bot,
        media_type='application/zip',
        headers={
            'Content-Disposition': 'attachment; filename=bot.zip',
        }
    )

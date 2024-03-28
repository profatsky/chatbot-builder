import io
import os
import zipfile

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.dialogues_schemas import DialogueWithBlocksReadSchema
from src.services import code_generation_service
from src.services.exceptions import projects_exceptions, dialogues_exceptions

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
        bot_code = await code_generation_service.get_bot_code(user_id, project_id, session)
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

    # TODO refactor after finishing bot-plugins
    in_memory_file = io.BytesIO(str.encode(bot_code))

    zip_data = io.BytesIO()

    with zipfile.ZipFile(zip_data, mode='w') as zipf:
        zipf.writestr('handlers/custom.py', in_memory_file.getvalue())

        main_file = 'src/bot_templates/project_structure/main.py.j2'
        zipf.write(main_file, 'main.py')

        loader_file = 'src/bot_templates/project_structure/loader.py.j2'
        zipf.write(loader_file, 'loader.py')

        config_file = 'src/bot_templates/project_structure/config.py.j2'
        zipf.write(config_file, 'config.py')

        db_file = 'src/bot_templates/project_structure/db.py.j2'
        zipf.write(db_file, 'db.py')

        middlewares_file = 'src/bot_templates/project_structure/middlewares.py.j2'
        zipf.write(middlewares_file, 'middlewares.py')

        env_file = 'src/bot_templates/project_structure/.env.example.j2'
        zipf.write(env_file, '.env.example')

        handlers_init_file = 'src/bot_templates/project_structure/handlers/__init__.py.j2'
        zipf.write(handlers_init_file, 'handlers/__init__.py')

    zip_data.seek(0)

    return StreamingResponse(
        zip_data,
        media_type='application/zip',
        headers={'Content-Disposition': 'attachment; filename=bot.zip'}
    )

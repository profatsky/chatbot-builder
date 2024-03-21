import io

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.dialogues_schemas import DialogueReadSchemaWithBlocks
from src.schemas.projects_schemas import ProjectReadSchema, ProjectCreateSchema, ProjectUpdateSchema
from src.services import projects_service, dialogues_service

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
)


@router.post('', response_model=ProjectReadSchema, status_code=status.HTTP_201_CREATED)
async def create_project(
        project_data: ProjectCreateSchema,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    project = await projects_service.create_project(user_id, project_data, session)
    return project


@router.get('', response_model=list[ProjectReadSchema])
async def get_projects(
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    projects = await projects_service.get_projects(user_id, session)
    return projects


@router.put('/{project_id}', response_model=ProjectReadSchema)
async def update_project(
        project_id: int,
        project_data: ProjectUpdateSchema,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    project = await projects_service.update_project(
        user_id=user_id,
        project_id=project_id,
        project_data=project_data,
        session=session,
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project does not exist',
        )

    return project


@router.delete('/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    await projects_service.delete_project(user_id, project_id, session)
    return {'message': 'Project was successfully deleted'}


@router.get('/{project_id}/code', response_model=list[DialogueReadSchemaWithBlocks])
async def get_bot_code(
        project_id: int,
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

    dialogues = await dialogues_service.get_dialogues(project_id, session)
    if not dialogues:
        HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='There are no dialogues in the project!'
        )

    file_data = await projects_service.get_code(dialogues)
    in_memory_file = io.BytesIO(str.encode(file_data))
    return StreamingResponse(io.BytesIO(in_memory_file.read()), media_type='text/plain')

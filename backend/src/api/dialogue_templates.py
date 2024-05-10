from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Query, status, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.dialogue_templates_schemas import DialogueTemplateReadSchema
from src.services import dialogue_templates_service
from src.services.exceptions import dialogue_templates_exceptions, projects_exceptions

router = APIRouter(
    tags=['templates'],
)


@router.get('/templates', response_model=list[DialogueTemplateReadSchema])
async def get_dialogue_templates(
        page: int = Query(ge=1, default=1),
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()

    templates = await dialogue_templates_service.get_templates(page, session)
    return templates


@router.get('/templates/{template_id}', response_model=DialogueTemplateReadSchema)
async def get_dialogue_template(
        template_id: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep)
):
    await auth_jwt.jwt_required()

    try:
        dialogue_template = await dialogue_templates_service.get_template(template_id, session)
    except dialogue_templates_exceptions.DialogueTemplateNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The specified dialogue template does not exist'
        )
    return dialogue_template


@router.post('/projects/{project_id}/templates', status_code=status.HTTP_201_CREATED)
async def add_dialogue_template_to_project(
        project_id: int,
        template_id: int = Body(embed=True),
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await dialogue_templates_service.check_access_and_create_dialogue_from_template(
            user_id=user_id,
            project_id=project_id,
            template_id=template_id,
            session=session,
        )
    except projects_exceptions.ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The specified project does not exist',
        )
    except projects_exceptions.NoPermissionForProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )
    except dialogue_templates_exceptions.DialogueTemplateNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The specified dialogue template does not exists',
        )

from typing import Annotated

from fastapi import APIRouter, Query, status, HTTPException, Body

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.dialogue_templates.dependencies.services_dependencies import DialogueTemplateServiceDI
from src.dialogue_templates.schemas import DialogueTemplateReadSchema
from src.dialogue_templates import exceptions as dialogue_templates_exceptions
from src.projects import exceptions as projects_exceptions

router = APIRouter(
    tags=['templates'],
)


@router.get('/templates', response_model=list[DialogueTemplateReadSchema])
async def get_dialogue_templates(
        auth_jwt: AuthJWTDI,
        dialogue_template_service: DialogueTemplateServiceDI,
        page: Annotated[int, Query(ge=1)] = 1,
):
    await auth_jwt.jwt_required()

    templates = await dialogue_template_service.get_templates(page)
    return templates


@router.get('/templates/{template_id}', response_model=DialogueTemplateReadSchema)
async def get_dialogue_template(
        template_id: int,
        auth_jwt: AuthJWTDI,
        dialogue_template_service: DialogueTemplateServiceDI,
):
    await auth_jwt.jwt_required()

    try:
        dialogue_template = await dialogue_template_service.get_template(template_id)
    except dialogue_templates_exceptions.DialogueTemplateNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The specified dialogue template does not exist'
        )
    return dialogue_template


@router.post('/projects/{project_id}/templates', status_code=status.HTTP_201_CREATED)
async def add_dialogue_template_to_project(
        project_id: int,
        template_id: Annotated[int, Body(embed=True)],
        auth_jwt: AuthJWTDI,
        dialogue_template_service: DialogueTemplateServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await dialogue_template_service.check_access_and_create_dialogue_from_template(
            user_id=user_id,
            project_id=project_id,
            template_id=template_id,
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

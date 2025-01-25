from typing import Annotated

from fastapi import APIRouter, Query, status, Body

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.dialogue_templates.dependencies.services_dependencies import DialogueTemplateServiceDI
from src.dialogue_templates.exceptions.http_exceptions import DialogueTemplateNotFoundHTTPException
from src.dialogue_templates.exceptions.services_exceptions import DialogueTemplateNotFoundError
from src.dialogue_templates.schemas import DialogueTemplateReadSchema
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException, NoPermissionForProjectHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError

router = APIRouter(
    tags=['Templates'],
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
    except DialogueTemplateNotFoundError:
        raise DialogueTemplateNotFoundHTTPException

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
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueTemplateNotFoundError:
        raise DialogueTemplateNotFoundHTTPException

from fastapi import APIRouter, status

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.projects.dependencies.services_dependencies import ProjectServiceDI
from src.projects.exceptions.http_exceptions import (
    ProjectNotFoundHTTPException,
    NoPermissionForProjectHTTPException,
    ProjectsLimitExceededHTTPException,
)
from src.projects.exceptions.services_exceptions import (
    ProjectsLimitExceededError,
    ProjectNotFoundError,
    NoPermissionForProjectError,
)
from src.projects.schemas import ProjectCreateSchema, ProjectUpdateSchema, ProjectReadSchema

router = APIRouter(
    prefix='/projects',
    tags=['Projects'],
)


@router.post(
    '',
    response_model=ProjectReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
        project_data: ProjectCreateSchema,
        auth_jwt: AuthJWTDI,
        project_service: ProjectServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        project = await project_service.create_project(
            user_id=user_id,
            project_data=project_data,
        )
    except ProjectsLimitExceededError:
        raise ProjectsLimitExceededHTTPException

    return project


@router.get('', response_model=list[ProjectReadSchema])
async def get_projects(
        auth_jwt: AuthJWTDI,
        project_service: ProjectServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    projects = await project_service.get_projects(user_id)
    return projects


@router.put('/{project_id}', response_model=ProjectReadSchema)
async def update_project(
        project_id: int,
        project_data: ProjectUpdateSchema,
        auth_jwt: AuthJWTDI,
        project_service: ProjectServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        project = await project_service.check_access_and_update_project(
            user_id=user_id,
            project_id=project_id,
            project_data=project_data,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    return project


@router.delete('/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
        project_id: int,
        auth_jwt: AuthJWTDI,
        project_service: ProjectServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await project_service.delete_project(
            user_id=user_id,
            project_id=project_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    return {'message': 'Project was successfully deleted'}

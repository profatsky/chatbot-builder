from fastapi import APIRouter, status, HTTPException

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.projects.dependencies.services_dependencies import ProjectServiceDI
from src.projects.schemas import ProjectCreateSchema, ProjectUpdateSchema, ProjectReadSchema
from src.projects import exceptions as projects_exceptions

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
)


@router.post('', response_model=ProjectReadSchema, status_code=status.HTTP_201_CREATED)
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
    except projects_exceptions.ProjectsLimitExceeded:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have the maximum number of projects',
        )
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

    return {'message': 'Project was successfully deleted'}

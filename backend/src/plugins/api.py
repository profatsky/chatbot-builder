from typing import Annotated

from fastapi import APIRouter, Query, status, HTTPException, Body

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.plugins.dependencies.services_dependencies import PluginServiceDI
from src.plugins.schemas import PluginReadSchema, PluginCreateSchema
from src.plugins import exceptions as plugins_exceptions
from src.users import exceptions as users_exceptions
from src.projects import exceptions as projects_exceptions

router = APIRouter(
    tags=['plugins'],
)


@router.post('/plugins', response_model=PluginReadSchema)
async def create_plugin(
        plugin_data: PluginCreateSchema,
        auth_jwt: AuthJWTDI,
        plugin_service: PluginServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        plugin = await plugin_service.check_access_and_create_plugin(
            user_id=user_id,
            plugin_data=plugin_data,
        )
    except users_exceptions.UserDoesNotHavePermission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )

    return plugin


@router.get('/plugins', response_model=list[PluginReadSchema])
async def get_plugins(
        auth_jwt: AuthJWTDI,
        plugin_service: PluginServiceDI,
        page: Annotated[int, Query(ge=1)] = 1,
):
    await auth_jwt.jwt_required()

    plugins = await plugin_service.get_plugins(page)
    return plugins


@router.get('/plugins/{plugin_id}', response_model=PluginReadSchema)
async def get_plugin(
        plugin_id: int,
        auth_jwt: AuthJWTDI,
        plugin_service: PluginServiceDI,
):
    await auth_jwt.jwt_required()

    try:
        plugin = await plugin_service.get_plugin(plugin_id)
    except plugins_exceptions.PluginNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The specified plugin does not exist',
        )
    return plugin


@router.delete('/plugins/{plugin_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_plugin(
        plugin_id: int,
        auth_jwt: AuthJWTDI,
        plugin_service: PluginServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await plugin_service.check_access_and_delete_plugin(
            user_id=user_id,
            plugin_id=plugin_id,
        )
    except users_exceptions.UserDoesNotHavePermission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )


@router.post('/projects/{project_id}/plugins', status_code=status.HTTP_201_CREATED)
async def add_plugin_to_project(
        project_id: int,
        plugin_id: Annotated[int, Body(embed=True)],
        auth_jwt: AuthJWTDI,
        plugin_service: PluginServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await plugin_service.check_access_and_add_plugin_to_project(
            user_id=user_id,
            project_id=project_id,
            plugin_id=plugin_id,
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
    except plugins_exceptions.PluginAlreadyInProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The specified plugin is already in the project',
        )
    except plugins_exceptions.PluginNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The specified plugin does not exits',
        )


@router.delete('/projects/{project_id}/plugins/{plugin_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_plugin_from_project(
        project_id: int,
        plugin_id: int,
        auth_jwt: AuthJWTDI,
        plugin_service: PluginServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await plugin_service.check_access_and_remove_plugin_from_project(
            user_id=user_id,
            project_id=project_id,
            plugin_id=plugin_id,
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
    except plugins_exceptions.PluginIsNotInProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The specified plugin is not in the project'
        )

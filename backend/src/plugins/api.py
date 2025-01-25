from typing import Annotated

from fastapi import APIRouter, Query, status, HTTPException, Body

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.plugins.dependencies.services_dependencies import PluginServiceDI
from src.plugins.exceptions.http_exceptions import (
    PluginNotFoundHTTPException,
    PluginAlreadyInProjectHTTPException,
    PluginIsNotInProjectHTTPException,
)
from src.plugins.exceptions.services_exceptions import (
    PluginNotFoundError,
    PluginAlreadyInProjectError,
    PluginIsNotInProjectError,
)
from src.plugins.schemas import PluginReadSchema, PluginCreateSchema
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException, NoPermissionForProjectHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError
from src.users.exceptions import UserDoesNotHavePermissionError

router = APIRouter(
    tags=['Plugins'],
)


@router.post(
    '/plugins',
    response_model=PluginReadSchema,
    status_code=status.HTTP_201_CREATED,
)
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
    except UserDoesNotHavePermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Dont have permission',
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
    except PluginNotFoundError:
        raise PluginNotFoundHTTPException

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
    except UserDoesNotHavePermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Dont have permission',
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

    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except PluginAlreadyInProjectError:
        raise PluginAlreadyInProjectHTTPException

    except PluginNotFoundError:
        raise PluginNotFoundHTTPException


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

    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except PluginIsNotInProjectError:
        raise PluginIsNotInProjectHTTPException

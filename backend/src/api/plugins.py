from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Query, status, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.plugins_schemas import PluginReadSchema, PluginCreateSchema
from src.services import plugins_service
from src.services.exceptions import projects_exceptions, plugins_exceptions, users_exceptions

router = APIRouter(
    tags=['plugins'],
)


@router.post('/plugins', response_model=PluginReadSchema)
async def create_plugin(
        plugin_data: PluginCreateSchema,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        plugin = await plugins_service.check_access_and_create_plugin(
            user_id=user_id,
            plugin_data=plugin_data,
            session=session,
        )
    except users_exceptions.UserDoesNotHavePermission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )

    return plugin


@router.get('/plugins', response_model=list[PluginReadSchema])
async def get_plugins(
        page: int = Query(ge=1, default=1),
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()

    plugins = await plugins_service.get_plugins(page, session)
    return plugins


@router.get('/plugins/{plugin_id}', response_model=PluginReadSchema)
async def get_plugin(
        plugin_id: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()

    plugin = await plugins_service.get_plugin(plugin_id, session)
    return plugin


@router.delete('/plugins/{plugin_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_plugin(
        plugin_id: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await plugins_service.check_access_and_delete_plugin(
            user_id=user_id,
            plugin_id=plugin_id,
            session=session,
        )
    except users_exceptions.UserDoesNotHavePermission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )


@router.post('/projects/{project_id}/plugins', status_code=status.HTTP_201_CREATED)
async def add_plugin_to_project(
        project_id: int,
        plugin_id: int = Body(embed=True),
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await plugins_service.check_access_and_add_plugin_to_project(
            user_id=user_id,
            project_id=project_id,
            plugin_id=plugin_id,
            session=session,
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
    except plugins_exceptions.PluginAlreadyInProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The specified plugin is already in the project'
        )


@router.delete('/projects/{project_id}/plugins/{plugin_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_plugin_from_project(
        project_id: int,
        plugin_id: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await plugins_service.check_access_and_remove_plugin_from_project(
            user_id=user_id,
            project_id=project_id,
            plugin_id=plugin_id,
            session=session,
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
    except plugins_exceptions.PluginIsNotInProject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The specified plugin is not in the project'
        )

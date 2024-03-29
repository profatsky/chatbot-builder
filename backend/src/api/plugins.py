from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.plugins_schemas import PluginReadSchema
from src.services import plugins_service

router = APIRouter(
    tags=['plugins'],
)


@router.get('/plugins', response_model=list[PluginReadSchema])
async def get_plugins(
        page: int = Query(ge=1, default=1),
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()

    plugins = await plugins_service.get_plugins(page, session)
    return plugins

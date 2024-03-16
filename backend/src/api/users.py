from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.users_schemas import UserReadSchema
from src.services import users_service
from src.services import auth_service

router = APIRouter(
    prefix='/users',
    tags=['auth'],
)


@router.get('/me', response_model=UserReadSchema)
async def get_user(
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    user = await users_service.get_user_by_id(user_id, session)
    if user is None:
        await auth_service.unset_auth_tokens(auth_jwt)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Missing cookie access_token_cookie.'
        )

    return user

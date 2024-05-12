from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.statistics_schemas import StatisticSchema
from src.services import statistics_service
from src.services.exceptions import users_exceptions

router = APIRouter(
    prefix='/statistics',
    tags=['statistics']
)


@router.get('', response_model=StatisticSchema)
async def get_statistic(
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        statistics = await statistics_service.check_access_and_get_statistic(user_id, session)
    except users_exceptions.UserDoesNotHavePermission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Don\t have permission',
        )

    return statistics

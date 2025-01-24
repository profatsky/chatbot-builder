from fastapi import APIRouter, HTTPException, status

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.statistics.dependencies.services_dependencies import StatisticServiceDI
from src.statistics.schemas import StatisticSchema
from src.users import exceptions as users_exceptions


router = APIRouter(
    prefix='/statistics',
    tags=['Statistics'],
)


@router.get('', response_model=StatisticSchema)
async def get_statistic(
        auth_jwt: AuthJWTDI,
        statistic_service: StatisticServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        statistics = await statistic_service.check_access_and_get_statistic(user_id)
    except users_exceptions.UserDoesNotHavePermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Dont have permission',
        )

    return statistics

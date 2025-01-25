from fastapi import APIRouter

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.statistics.dependencies.services_dependencies import StatisticServiceDI
from src.statistics.schemas import StatisticSchema
from src.users.exceptions.http_exceptions import DontHavePermissionHTTPException
from src.users.exceptions.services_exceptions import DontHavePermissionError

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
    except DontHavePermissionError:
        raise DontHavePermissionHTTPException

    return statistics

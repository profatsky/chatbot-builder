from fastapi import APIRouter, HTTPException, status

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.auth.dependencies.services_dependencies import AuthServiceDI
from src.users.dependencies.services_dependencies import UserServiceDI
from src.users.schemas import UserWithStatsReadSchema
from src.users import exceptions as users_exceptions

router = APIRouter(
    prefix='/users',
    tags=['auth'],
)


@router.get('/me', response_model=UserWithStatsReadSchema)
async def get_user(
        auth_jwt: AuthJWTDI,
        user_service: UserServiceDI,
        auth_service: AuthServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        user = await user_service.get_user_with_stats(user_id)
    except users_exceptions.UserNotFound:
        await auth_service.unset_auth_tokens()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized user'
        )

    return user

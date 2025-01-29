from fastapi import APIRouter, HTTPException, status

from src.auth.dependencies.services_dependencies import AuthServiceDI
from src.auth.schemas import AuthCredentialsSchema
from src.users.dependencies.services_dependencies import UserServiceDI
from src.users.exceptions.http_exceptions import UserAlreadyExistsHTTPException
from src.users.exceptions.services_exceptions import UserAlreadyExistsError, InvalidCredentialsError

router = APIRouter(tags=['Auth'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
        credentials: AuthCredentialsSchema,
        auth_service: AuthServiceDI,
        user_service: UserServiceDI,
):
    try:
        user = await user_service.create_user(credentials)
    except UserAlreadyExistsError:
        raise UserAlreadyExistsHTTPException

    await auth_service.set_auth_tokens(user.user_id)
    return {'detail': 'Registration was successful'}


@router.post('/login')
async def login(
        credentials: AuthCredentialsSchema,
        auth_service: AuthServiceDI,
        user_service: UserServiceDI,
):
    try:
        user = await user_service.get_user_by_credentials(credentials)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
        )

    await auth_service.set_auth_tokens(user.user_id)
    return {'detail': 'Authorization was successful'}


# Нужно отправлять csrf_refresh_token в заголовке X-CSRF-Token
@router.post('/refresh')
async def refresh(
        auth_service: AuthServiceDI,
):
    await auth_service.refresh_access_token()
    return {'detail': 'Refresh access token was successful'}


# Нужно отправлять csrf_access_token в заголовке X-CSRF-Token
@router.post('/logout')
async def logout(
        auth_service: AuthServiceDI,
):
    await auth_service.unset_auth_tokens()
    return {'detail': 'Logout was successful'}

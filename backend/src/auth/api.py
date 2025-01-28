from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Body
from pydantic import EmailStr

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.auth.dependencies.services_dependencies import AuthServiceDI
from src.auth.schemas import AuthCredentialsSchema, Password
from src.core import settings
from src.users.dependencies.services_dependencies import UserServiceDI
from src.users.exceptions.http_exceptions import UserAlreadyExistsHTTPException
from src.users.exceptions.services_exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidCredentialsError,
)

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


# Нужно отправлять csrf_access_token в заголовке X-CSRF-Token
@router.post('/request-email-verification')
async def request_email_verification(
        auth_jwt: AuthJWTDI,
        auth_service: AuthServiceDI,
        user_service: UserServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        user = await user_service.get_user_by_id(user_id)
    except UserNotFoundError:
        await auth_service.unset_auth_tokens()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized user'
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Email already verified'
        )

    auth_service.create_and_save_email_verification_code(user_id)
    verification_code = auth_service.get_email_verification_code(user_id)

    await auth_service.send_email_with_email_verification(
        user_id=user_id,
        recipient_email=user.email,
        verification_code=verification_code,
    )

    # TODO remove print
    print(f'{settings.CLIENT_APP_URL}/verify-email?user_id={user_id}&code={verification_code}')
    return {'detail': 'Verification was requested'}


@router.get('/verify-email')
async def verify_email(
        user_id: int,
        code: int,
        auth_service: AuthServiceDI,
        user_service: UserServiceDI,
):
    saved_code = auth_service.get_email_verification_code(user_id)
    if saved_code is None or saved_code != code:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid code specified'
        )

    auth_service.remove_email_verification_code(user_id)

    try:
        user = await user_service.set_verified_status_for_user(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User with specified id does not exists'
        )

    await auth_service.set_auth_tokens(user.user_id)

    return {'detail': 'Email verification was successful'}


# Нужно отправлять csrf_access_token в заголовке X-CSRF-Token
@router.post('/request-email-change')
async def request_email_change(
        new_email: Annotated[EmailStr, Body(embed=True)],
        auth_jwt: AuthJWTDI,
        auth_service: AuthServiceDI,
        user_service: UserServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    user_with_same_email = await user_service.get_user_by_email(new_email)
    if user_with_same_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User with this email already exists'
        )

    user = await user_service.get_user_by_id(user_id)
    if not user.is_verified:
        user = await user_service.change_user_email_and_set_unverified_status(
            user_id=user_id,
            new_email=new_email,
        )
        await auth_service.set_auth_tokens(user.user_id)
        return {'detail': 'Your last email was not verified. Email change was successful'}

    auth_service.create_and_save_email_change_verification_code(user_id, new_email)
    verification_code, _ = auth_service.get_email_and_change_verification_code(user_id)

    await auth_service.send_email_with_email_change_request(
        user_id=user_id,
        recipient_email=user.email,
        verification_code=verification_code,
        new_email=new_email,
    )

    # TODO remove print
    print(f'{settings.CLIENT_APP_URL}/verify-email-change?user_id={user_id}&code={verification_code}')
    return {'message': 'Email change was requested'}


@router.get('/verify-email-change')
async def verify_email_change(
        user_id: int,
        code: int,
        auth_jwt: AuthJWTDI,
        auth_service: AuthServiceDI,
        user_service: UserServiceDI,
):
    try:
        saved_code, new_email = auth_service.get_email_and_change_verification_code(user_id)
        if saved_code != code:
            raise ValueError
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid code specified'
        )

    auth_service.remove_email_change_verification_code(user_id)

    user = await user_service.change_user_email_and_set_unverified_status(
        user_id=user_id,
        new_email=new_email,
    )
    await auth_service.set_auth_tokens(user.user_id, auth_jwt)

    return {'detail': 'Email change was successful'}


# Нужно отправлять csrf_access_token в заголовке X-CSRF-Token
@router.post('/request-change-password')
async def request_change_password(
        new_password: Annotated[Password, Body(embed=True)],
        auth_jwt: AuthJWTDI,
        auth_service: AuthServiceDI,
        user_service: UserServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        user = await user_service.get_user_by_id(user_id)
    except UserNotFoundError:
        await auth_service.unset_auth_tokens()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized user'
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You can not change your password until you confirm your email'
        )

    auth_service.create_and_save_password_change_verification_code(user_id, new_password)
    verification_code, _ = auth_service.get_password_and_change_verification_code(user_id)

    await auth_service.send_email_with_password_change_request(
        user_id=user_id,
        recipient_email=user.email,
        verification_code=verification_code,
    )

    # TODO remove print
    print(f'{settings.CLIENT_APP_URL}/verify-password-change?user_id={user_id}&code={verification_code}')
    return {'detail': 'Password change was requested'}


@router.get('/verify-password-change')
async def verify_password_change(
        user_id: int,
        code: int,
        auth_service: AuthServiceDI,
        user_service: UserServiceDI,
):
    try:
        saved_code, new_password = auth_service.get_password_and_change_verification_code(user_id)
        if saved_code != code:
            raise ValueError
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid code specified'
        )

    auth_service.remove_password_change_verification_code(user_id)

    try:
        user = await user_service.change_user_password(
            user_id=user_id,
            new_password=new_password,
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User with specified id does not exists'
        )

    await auth_service.set_auth_tokens(user.user_id)

    return {'detail': 'Password change was successful'}


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
            detail='Неверные данные для входа!'
        )

    await auth_service.set_auth_tokens(user.user_id)
    return {'detail': 'Авторизация прошла успешно!'}


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

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.params import Body
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import settings
from src.core.auth import auth_dep
from src.core.db import get_async_session
from src.schemas.auth_schemas import AuthCredentialsSchema, Password
from src.services import auth_service, users_service

router = APIRouter(tags=['auth'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
        credentials: AuthCredentialsSchema,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    user = await users_service.create_new_user(credentials, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email already exists.'
        )

    await auth_service.set_auth_tokens(user, auth_jwt)
    return {'message': 'Registration was successful.'}


# Нужно отправлять csrf_access_token в заголовке X-CSRF-Token
@router.post('/request-email-verification')
async def request_email_verification(
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    user = await users_service.get_user_by_id(user_id, session)
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Email already verified.'
        )

    auth_service.create_and_save_email_verification_code(user_id)
    verification_code = auth_service.get_email_verification_code(user_id)

    await auth_service.send_email_with_email_verification(
        user_id=user_id,
        recipient_email=user.email,
        verification_code=verification_code,
    )

    # TODO remove print
    print(f'{settings.BASE_URL}/verify-email?user_id={user_id}&code={verification_code}')
    return {'message': 'Verification was requested.'}


@router.get('/verify-email')
async def verify_email(
        user_id: int,
        code: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    saved_code = auth_service.get_email_verification_code(user_id)
    if saved_code is None or saved_code != code:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid code specified.'
        )

    auth_service.remove_email_verification_code(user_id)

    user = await users_service.set_verified_status_for_user(user_id, session)
    await auth_service.set_auth_tokens(user, auth_jwt)

    return {'message': 'Email verification was successful.'}


# Нужно отправлять csrf_access_token в заголовке X-CSRF-Token
@router.post('/request-email-change')
async def request_email_change(
        new_email: EmailStr = Body(embed=True),
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    user_with_same_email = await users_service.get_user_by_email(new_email, session)
    if user_with_same_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User with this email already exists.'
        )

    user = await users_service.get_user_by_id(user_id, session)
    if not user.is_verified:
        user = await users_service.change_user_email_and_set_unverified_status(
            user_id=user_id,
            new_email=new_email,
            session=session,
        )
        await auth_service.set_auth_tokens(user, auth_jwt)
        return {'message': 'Your last email was not verified. Email change was successful.'}

    auth_service.create_and_save_email_change_verification_code(user_id, new_email)
    verification_code, _ = auth_service.get_email_and_change_verification_code(user_id)

    await auth_service.send_email_with_email_change_request(
        user_id=user_id,
        recipient_email=user.email,
        verification_code=verification_code,
        new_email=new_email,
    )

    # TODO remove print
    print(f'{settings.BASE_URL}/verify-email-change?user_id={user_id}&code={verification_code}')
    return {'message': 'Email change was requested.'}


@router.get('/verify-email-change')
async def verify_email_change(
        user_id: int,
        code: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    try:
        saved_code, new_email = auth_service.get_email_and_change_verification_code(user_id)
        if saved_code != code:
            raise ValueError
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid code specified.'
        )

    auth_service.remove_email_change_verification_code(user_id)

    user = await users_service.change_user_email_and_set_unverified_status(
        user_id=user_id,
        new_email=new_email,
        session=session,
    )
    await auth_service.set_auth_tokens(user, auth_jwt)

    return {'message': 'Email change was successful.'}


# Нужно отправлять csrf_access_token в заголовке X-CSRF-Token
@router.post('/request-change-password')
async def request_change_password(
        new_password: Password = Body(embed=True),
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    user = await users_service.get_user_by_id(user_id, session)
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
    print(f'{settings.BASE_URL}/verify-password-change?user_id={user_id}&code={verification_code}')
    return {'message': 'Password change was requested.'}


@router.get('/verify-password-change')
async def verify_password_change(
        user_id: int,
        code: int,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    try:
        saved_code, new_password = auth_service.get_password_and_change_verification_code(user_id)
        if saved_code != code:
            raise ValueError
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid code specified.'
        )

    auth_service.remove_password_change_verification_code(user_id)

    user = await users_service.change_user_password(
        user_id=user_id,
        new_password=new_password,
        session=session,
    )
    await auth_service.set_auth_tokens(user, auth_jwt)

    return {'message': 'Password change was successful.'}


@router.post('/login')
async def login(
        credentials: AuthCredentialsSchema,
        session: AsyncSession = Depends(get_async_session),
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    user = await users_service.get_user_by_credentials(credentials, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials.'
        )

    await auth_service.set_auth_tokens(user, auth_jwt)
    return {'message': 'Login was successful.'}


# Нужно отправлять csrf_refresh_token в заголовке X-CSRF-Token
@router.post('/refresh')
async def refresh(
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_service.refresh_access_token(auth_jwt)
    return {'message': 'Refresh access token was successful.'}


# Нужно отправлять csrf_access_token в заголовке X-CSRF-Token
@router.post('/logout')
async def logout(
        auth_jwt: AuthJWT = Depends(auth_dep),
):
    await auth_service.unset_auth_tokens(auth_jwt)
    return {'message': 'Logout was successful.'}

from fastapi import APIRouter, status, Body, Depends, HTTPException
from fastapi_users import FastAPIUsers, exceptions
from fastapi.requests import Request
from pydantic import EmailStr

from src.core.auth import auth_backend
from src.models import UserModel
from src.schemas.users import UserRead, UserCreate
from src.services.auth_service import InvalidEmailChangeToken, get_auth_service, AuthService

fastapi_users = FastAPIUsers[UserModel, int](
    get_auth_service,
    [auth_backend],
)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/jwt'
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
)
router.include_router(
    fastapi_users.get_reset_password_router(),
)


@router.post(
    '/request-email-change',
    status_code=status.HTTP_202_ACCEPTED,
)
async def request_email_change(
    request: Request,
    email: EmailStr = Body(..., embed=True),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user = await auth_service.get_by_email(email)
    except exceptions.UserNotExists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    try:
        await auth_service.request_email_change(user, request)
    except exceptions.UserInactive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post(
    '/change-email',
    status_code=status.HTTP_200_OK
)
async def change_email(
    request: Request,
    new_email: EmailStr = Body(...),
    token: str = Body(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        await auth_service.change_email(token, new_email, request)
    except (
        InvalidEmailChangeToken,
        exceptions.UserInactive,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

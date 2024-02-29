from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from src.core.auth import auth_backend
from src.models import UserModel
from src.schemas.users import UserRead, UserCreate
from src.services.users import get_user_manager

fastapi_users = FastAPIUsers[UserModel, int](
    get_user_manager,
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


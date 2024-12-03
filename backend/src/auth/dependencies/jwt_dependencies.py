from typing import Annotated

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends

from src.core.auth import auth_dep

AuthJWTDI = Annotated[AuthJWT, Depends(auth_dep)]

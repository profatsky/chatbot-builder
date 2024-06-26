from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer, AuthJWT
from pydantic import BaseModel

from src.core import settings

auth_dep = AuthJWTBearer()


class AuthSettings(BaseModel):
    authjwt_secret_key: str = settings.JWT_SECRET
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = True
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_samesite: str = 'lax'


@AuthJWT.load_config
def get_config():
    return AuthSettings()

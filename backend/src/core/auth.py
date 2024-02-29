from fastapi_users.authentication import JWTStrategy, AuthenticationBackend

from src.core.settings import SECRET, TRANSPORT


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=36000)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=TRANSPORT,
    get_strategy=get_jwt_strategy,
)

from src.auth.dependencies.jwt_dependencies import AuthJWTDI


class AuthService:
    def __init__(self, auth_jwt: AuthJWTDI):
        self._auth_jwt = auth_jwt

    async def set_auth_tokens(self, user_id: int):
        access_token = await self._auth_jwt.create_access_token(subject=user_id)
        refresh_token = await self._auth_jwt.create_refresh_token(subject=user_id)

        await self._auth_jwt.set_access_cookies(access_token)
        await self._auth_jwt.set_refresh_cookies(refresh_token)

    async def refresh_access_token(self):
        await self._auth_jwt.jwt_refresh_token_required()

        user_id = await self._auth_jwt.get_jwt_subject()
        new_access_token = await self._auth_jwt.create_access_token(subject=user_id)

        await self._auth_jwt.set_access_cookies(new_access_token)

    async def unset_auth_tokens(self):
        await self._auth_jwt.jwt_required()
        await self._auth_jwt.unset_jwt_cookies()

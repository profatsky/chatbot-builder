import pytest
from httpx import AsyncClient


class TestUsersAPI:
    @pytest.mark.asyncio
    async def test_successful_get_me(self, authorized_client: AsyncClient):
        response = await authorized_client.get('/users/me')
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_unauthorized_get_me(self, client: AsyncClient):
        response = await client.get('/users/me')
        assert response.status_code == 401

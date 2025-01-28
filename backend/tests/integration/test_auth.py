import pytest
from httpx import AsyncClient

from src.users.schemas import UserReadSchema


class TestAuthAPI:
    @pytest.mark.asyncio
    async def test_successful_register(self, client: AsyncClient):
        payload = {
            'email': 'email@email.com',
            'password': 'password',
        }
        response = await client.post('/register', json=payload)
        assert response.status_code == 201
        assert response.json() == {'detail': 'Registration was successful'}

        set_cookie_header = response.headers.get('set-cookie')
        assert set_cookie_header
        assert 'access_token_cookie' in set_cookie_header
        assert 'refresh_token_cookie' in set_cookie_header

    @pytest.mark.asyncio
    async def test_register_existing_user(self, client: AsyncClient, test_user: UserReadSchema):
        payload = {
            'email': test_user.email,
            'password': 'password',
        }
        response = await client.post('/register', json=payload)

        assert response.status_code == 409
        assert response.json() == {'detail': 'User with this email address is already registered'}

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client: AsyncClient):
        payload = {
            'email': 'invalid-email',
            'password': 'password',
        }
        response = await client.post('/register', json=payload)
        assert response.status_code == 422

        error_location = response.json()['detail'][0]['loc']
        assert error_location == ['body', 'email']

    @pytest.mark.asyncio
    async def test_register_invalid_password(self, client: AsyncClient):
        payload = {
            'email': 'email@email.com',
            'password': '123',
        }
        response = await client.post('/register', json=payload)
        assert response.status_code == 422

        error_location = response.json()['detail'][0]['loc']
        assert error_location == ['body', 'password']

    @pytest.mark.asyncio
    async def test_register_missing_fields(self, client: AsyncClient):
        invalid_payloads = [
            {'email': 'missing-password@email.com'},
            {'password': 'missing-email'},
            {},
        ]
        for payload in invalid_payloads:
            response = await client.post('/register', json=payload)
            assert response.status_code == 422

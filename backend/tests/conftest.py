import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.auth.schemas import AuthCredentialsSchema
from src.core import settings
from src.core.db import Base, get_async_session, get_postgres_dsn
from src.enums import KeyboardType
from src.main import app
from src.projects.repositories import ProjectRepository
from src.projects.schemas import ProjectCreateSchema
from src.users.repositories import UserRepository
from src.users.schemas import UserReadSchema

SQLALCHEMY_DATABASE_URL = get_postgres_dsn(
    user=settings.DB_USER,
    password=settings.DB_PASS,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.TEST_DB_NAME,
)

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(
    expire_on_commit=False,
    bind=async_engine,
    class_=AsyncSession,
)

TEST_USER_CREDENTIALS = {
    'email': 'test@test.com',
    'password': 'password',
}


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if pytest_asyncio.is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope='session')
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest_asyncio.fixture(scope='session')
async def session():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope='session')
async def client(session) -> AsyncClient:
    async def override_get_session():
        try:
            yield session
        finally:
            await session.close()

    app.dependency_overrides[get_async_session] = override_get_session
    async with LifespanManager(app) as manager:
        async with AsyncClient(
                transport=ASGITransport(
                    app=manager.app
                ),
                base_url='http://127.0.0.1:8000/api',
        ) as cli:
            yield cli


@pytest_asyncio.fixture(scope='session')
async def user_repository(session) -> UserRepository:
    return UserRepository(session)


@pytest_asyncio.fixture(scope='session')
async def test_user(user_repository: UserRepository):
    credentials = AuthCredentialsSchema.model_validate(TEST_USER_CREDENTIALS)
    user = await user_repository.create_user(credentials)
    yield user
    await user_repository.delete_user(user.user_id)


@pytest_asyncio.fixture(scope='function', loop_scope='session')
async def authorized_client(client: AsyncClient, test_user: UserReadSchema) -> AsyncClient:
    response = await client.post('/login', json=TEST_USER_CREDENTIALS)

    access_token = response.json()['access_token']
    client.headers['Authorization'] = access_token
    yield client
    client.headers.pop('Authorization')


@pytest_asyncio.fixture(scope='session')
async def project_repository(session) -> ProjectRepository:
    return ProjectRepository(session)


@pytest_asyncio.fixture(scope='session')
async def project_data_for_create() -> ProjectCreateSchema:
    return ProjectCreateSchema(
        name='Test project',
        start_message='Test start message',
        start_keyboard_type=KeyboardType.REPLY_KEYBOARD.value,
    )

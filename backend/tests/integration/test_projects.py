import pytest
from httpx import AsyncClient

from src.projects.repositories import ProjectRepository
from src.users.schemas import UserReadSchema
from tests.factories.projects import ProjectCreateSchemaFactory
from tests.utils.projects import assert_project_response


class TestProjectsApi:
    @pytest.mark.asyncio
    async def test_successful_create_project(self, test_user: UserReadSchema, authorized_client: AsyncClient):
        project_data = ProjectCreateSchemaFactory()

        response = await authorized_client.post(
            '/projects',
            json=project_data.model_dump(mode='json'),
        )
        assert response.status_code == 201

        response_data = response.json()
        assert_project_response(
            response_data=response_data,
            expected_data=project_data,
            user_id=test_user.user_id,
        )

    @pytest.mark.asyncio
    async def test_create_project_limit_exceeded(
            self,
            test_user: UserReadSchema,
            authorized_client: AsyncClient,
            project_repository: ProjectRepository,
    ):
        for _ in range(5):
            await project_repository.create_project(
                user_id=test_user.user_id,
                project_data=ProjectCreateSchemaFactory(),
            )

        response = await authorized_client.post(
            '/projects',
            json=ProjectCreateSchemaFactory().model_dump(mode='json'),
        )

        assert response.status_code == 403
        assert response.json() == {'detail': 'Projects limit exceeded'}

    @pytest.mark.asyncio
    async def test_get_projects_successful(
            self,
            test_user: UserReadSchema,
            authorized_client: AsyncClient,
            project_repository: ProjectRepository,
    ):
        projects_data = [ProjectCreateSchemaFactory() for _ in range(5)]
        for project_data in projects_data:
            await project_repository.create_project(
                user_id=test_user.user_id,
                project_data=project_data,
            )

        response = await authorized_client.get('/projects')
        assert response.status_code == 200

        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == len(projects_data)

        for i, project_data in enumerate(projects_data):
            assert_project_response(
                response_data=response_data[i],
                expected_data=project_data,
                user_id=test_user.user_id,
            )

    @pytest.mark.asyncio
    async def test_get_projects_empty(self, authorized_client: AsyncClient):
        response = await authorized_client.get('/projects')
        assert response.status_code == 200
        assert response.json() == []

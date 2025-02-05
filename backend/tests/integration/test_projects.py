import pytest
from httpx import AsyncClient

from src.projects.repositories import ProjectRepository
from src.projects.schemas import ProjectReadSchema
from src.users.schemas import UserReadSchema
from tests.factories.projects import ProjectCreateSchemaFactory
from tests.utils.projects import assert_project_response


class TestProjectsApi:
    @pytest.mark.asyncio
    async def test_create_project_success(self, test_user: UserReadSchema, authorized_client: AsyncClient):
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
    @pytest.mark.parametrize('created_projects', [5], indirect=True)
    async def test_create_project_limit_exceeded(
            self,
            test_user: UserReadSchema,
            authorized_client: AsyncClient,
            created_projects: list[ProjectReadSchema],
    ):
        response = await authorized_client.post(
            '/projects',
            json=ProjectCreateSchemaFactory().model_dump(mode='json'),
        )

        assert response.status_code == 403
        assert response.json() == {'detail': 'Projects limit exceeded'}

    @pytest.mark.asyncio
    @pytest.mark.parametrize('created_projects', [5], indirect=True)
    async def test_get_projects_success(
            self,
            test_user: UserReadSchema,
            authorized_client: AsyncClient,
            project_repository: ProjectRepository,
            created_projects: list[ProjectReadSchema],
    ):
        response = await authorized_client.get('/projects')
        assert response.status_code == 200

        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == len(created_projects)

        for i, project_data in enumerate(created_projects):
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

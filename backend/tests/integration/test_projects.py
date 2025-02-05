import pytest
from httpx import AsyncClient

from src.projects.repositories import ProjectRepository
from src.projects.schemas import ProjectCreateSchema


class TestProjectsApi:
    @pytest.mark.asyncio
    async def test_successful_create_project(
            self,
            authorized_client: AsyncClient,
            project_data_for_create: ProjectCreateSchema,
    ):
        response = await authorized_client.post(
            '/projects',
            json=project_data_for_create.model_dump(mode='json'),
        )
        assert response.status_code == 201

        response_data = response.json()
        assert 'project_id' in response_data
        assert response_data['name'] == project_data_for_create.name
        assert response_data['start_message'] == project_data_for_create.start_message
        assert response_data['start_keyboard_type'] == project_data_for_create.start_keyboard_type.value

    @pytest.mark.asyncio
    async def test_create_project_limit_exceeded(
            self,
            test_user,
            authorized_client: AsyncClient,
            project_repository: ProjectRepository,
            project_data_for_create: ProjectCreateSchema,
    ):
        for _ in range(5):
            await project_repository.create_project(
                user_id=test_user.user_id,
                project_data=project_data_for_create,
            )
        response = await authorized_client.post(
            '/projects',
            json=project_data_for_create.model_dump(mode='json'),
        )

        assert response.status_code == 403
        assert response.json() == {'detail': 'Projects limit exceeded'}

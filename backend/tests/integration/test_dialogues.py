import pytest
from httpx import AsyncClient

from src.dialogues.repositories import DialogueRepository
from src.projects.schemas import ProjectReadSchema
from tests.factories.dialogues import DialogueCreateSchemaFactory


class TestDialoguesAPI:
    @pytest.mark.asyncio
    async def test_create_dialogue_success(
            self,
            authorized_test_client: AsyncClient,
            test_project: ProjectReadSchema,
    ):
        dialogue = DialogueCreateSchemaFactory()
        response = await authorized_test_client.post(
            f'/projects/{test_project.project_id}/dialogues',
            json=dialogue.model_dump(mode='json'),
        )
        assert response.status_code == 201

        response_data = response.json()
        assert 'dialogue_id' in response_data
        assert 'created_at' in response_data
        assert 'trigger_id' in response_data['trigger']
        assert response_data['trigger']['event_type'] == dialogue.trigger.event_type.value
        assert response_data['trigger']['value'] == dialogue.trigger.value

    @pytest.mark.asyncio
    async def test_create_dialogue_project_not_found(self, authorized_test_client: AsyncClient):
        dialogue = DialogueCreateSchemaFactory()
        response = await authorized_test_client.post(
            '/projects/999999/dialogues',
            json=dialogue.model_dump(mode='json'),
        )

        assert response.status_code == 404
        assert response.json() == {'detail': 'Project does not exist'}

    @pytest.mark.asyncio
    async def test_create_dialogue_no_permission(
            self,
            authorized_another_client: AsyncClient,
            test_project: ProjectReadSchema,
    ):
        dialogue = DialogueCreateSchemaFactory()
        response = await authorized_another_client.post(
            f'/projects/{test_project.project_id}/dialogues',
            json=dialogue.model_dump(mode='json'),
        )

        assert response.status_code == 403
        assert response.json() == {'detail': 'No permission for this project'}

    @pytest.mark.asyncio
    async def test_create_dialogue_limit_exceeded(
            self,
            authorized_test_client: AsyncClient,
            test_project: ProjectReadSchema,
            dialogue_repository: DialogueRepository,
    ):
        for _ in range(10):
            await dialogue_repository.create_dialogue(
                project_id=test_project.project_id,
                dialogue_data=DialogueCreateSchemaFactory(),
            )

        response = await authorized_test_client.post(
            f'/projects/{test_project.project_id}/dialogues',
            json=DialogueCreateSchemaFactory().model_dump(mode='json'),
        )

        assert response.status_code == 403
        assert response.json() == {'detail': 'Dialogues limit exceeded'}

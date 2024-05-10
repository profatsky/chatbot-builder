from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence import dialogue_templates_persistence
from src.schemas.dialogue_templates_schemas import DialogueTemplateReadSchema
from src.services import projects_service
from src.services.exceptions import dialogue_templates_exceptions

DIALOGUE_TEMPLATES_PER_PAGE = 9


async def get_templates(
        page: int,
        session: AsyncSession,
) -> list[DialogueTemplateReadSchema]:
    templates = await dialogue_templates_persistence.get_templates(
        offset=(page - 1) * DIALOGUE_TEMPLATES_PER_PAGE,
        limit=DIALOGUE_TEMPLATES_PER_PAGE,
        session=session,
    )
    return templates


async def get_template(
        template_id: int,
        session: AsyncSession,
) -> DialogueTemplateReadSchema:
    template = await dialogue_templates_persistence.get_template(
        template_id, session
    )
    if template is None:
        raise dialogue_templates_exceptions.DialogueTemplateNotFound

    return template


async def check_access_and_create_dialogue_from_template(
        user_id: int,
        project_id: int,
        template_id: int,
        session: AsyncSession,
):
    _ = await projects_service.check_access_and_get_project(
        user_id=user_id,
        project_id=project_id,
        session=session,
    )

    _ = await get_template(template_id, session)

    await dialogue_templates_persistence.create_dialogue_from_template(
        project_id=project_id,
        template_id=template_id,
        session=session,
    )

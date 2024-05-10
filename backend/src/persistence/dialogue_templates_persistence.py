from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, DeclarativeBase

from src.models import DialogueModel, BlockModel, TriggerModel
from src.models.dialogue_templates import DialogueTemplateModel
from src.schemas.dialogue_templates_schemas import DialogueTemplateReadSchema
from src.utils import blocks_utils


async def get_templates(
        offset: int,
        limit: int,
        session: AsyncSession,
) -> list[DialogueTemplateReadSchema]:
    templates = await session.execute(
        select(DialogueTemplateModel)
        .order_by(DialogueTemplateModel.created_at)
        .offset(offset)
        .limit(limit)
    )
    templates = templates.scalars().all()
    return [DialogueTemplateReadSchema.model_validate(template) for template in templates]


async def get_template(
        template_id: int,
        session: AsyncSession,
) -> Optional[DialogueTemplateReadSchema]:
    template = await session.execute(
        select(DialogueTemplateModel)
        .where(DialogueTemplateModel.template_id == template_id)
    )
    template = template.scalar()
    if not template:
        return
    return DialogueTemplateReadSchema.model_validate(template)


async def create_dialogue_from_template(
        project_id: int,
        template_id: int,
        session: AsyncSession,
):
    template = await session.execute(
        select(DialogueTemplateModel)
        .options(
            joinedload(DialogueTemplateModel.dialogue)
            .options(
                joinedload(DialogueModel.trigger),
                selectinload(DialogueModel.blocks)
                .selectin_polymorphic(BlockModel.__subclasses__()),
            )
        )
        .where(DialogueTemplateModel.template_id == template_id)
    )
    template = template.scalar()

    trigger_in_template = template.dialogue.trigger
    new_trigger = TriggerModel(**_get_db_table_row(trigger_in_template))
    new_trigger.trigger_id = None

    dialogue_in_template = template.dialogue
    new_dialogue = DialogueModel(**_get_db_table_row(dialogue_in_template))
    new_dialogue.dialogue_id = None
    new_dialogue.project_id = project_id

    blocks_in_template = template.dialogue.blocks
    new_blocks = []
    for block in blocks_in_template:
        block_model = blocks_utils.get_block_model_by_type(block.type)
        new_block = block_model(**_get_db_table_row(block))
        new_block.block_id = None
        new_block.dialogue = new_dialogue
        new_blocks.append(new_block)

    session.add(new_trigger)
    session.add(new_dialogue)
    for block in new_blocks:
        session.add(block)

    await session.commit()


def _get_db_table_row(model_instance: DeclarativeBase) -> dict:
    table_row = {}
    for key, value in model_instance.__dict__.items():
        if key == '_sa_instance_state' or _is_relationship(value):
            continue
        table_row[key] = value

    return table_row


def _is_relationship(model_instance_field_value) -> bool:
    return (
        isinstance(model_instance_field_value, DeclarativeBase) or
        isinstance(model_instance_field_value, list)
    )

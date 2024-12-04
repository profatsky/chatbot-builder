from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload, DeclarativeBase

from src.blocks.models import BlockModel
from src.core.dependencies.db_dependencies import AsyncSessionDI
from src.dialogue_templates.models import DialogueTemplateModel
from src.dialogue_templates.schemas import DialogueTemplateReadSchema
from src.blocks import utils
from src.dialogues.models import DialogueModel, TriggerModel


class DialogueTemplateRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def get_templates(
            self,
            offset: int,
            limit: int,
    ) -> list[DialogueTemplateReadSchema]:
        templates = await self._session.execute(
            select(DialogueTemplateModel)
            .order_by(DialogueTemplateModel.created_at)
            .offset(offset)
            .limit(limit)
        )
        templates = templates.scalars().all()
        return [DialogueTemplateReadSchema.model_validate(template) for template in templates]

    async def get_template(
            self,
            template_id: int,
    ) -> Optional[DialogueTemplateReadSchema]:
        template = await self._session.execute(
            select(DialogueTemplateModel)
            .where(DialogueTemplateModel.template_id == template_id)
        )
        template = template.scalar()
        if not template:
            return
        return DialogueTemplateReadSchema.model_validate(template)

    async def create_dialogue_from_template(
            self,
            project_id: int,
            template_id: int,
    ):
        template = await self._session.execute(
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
        new_trigger = TriggerModel(**self._get_db_table_row(trigger_in_template))
        new_trigger.trigger_id = None

        dialogue_in_template = template.dialogue
        new_dialogue = DialogueModel(**self._get_db_table_row(dialogue_in_template))
        new_dialogue.dialogue_id = None
        new_dialogue.project_id = project_id

        blocks_in_template = template.dialogue.blocks
        new_blocks = []
        for block in blocks_in_template:
            block_model = utils.get_block_model_by_type(block.type)
            new_block = block_model(**self._get_db_table_row(block))
            new_block.block_id = None
            new_block.dialogue = new_dialogue
            new_blocks.append(new_block)

        self._session.add(new_trigger)
        self._session.add(new_dialogue)
        for block in new_blocks:
            self._session.add(block)

        await self._session.commit()

    def _get_db_table_row(self, model_instance: DeclarativeBase) -> dict:
        table_row = {}
        for key, value in model_instance.__dict__.items():
            if key == '_sa_instance_state' or self._is_relationship(value):
                continue
            table_row[key] = value

        return table_row

    @staticmethod
    def _is_relationship(model_instance_field_value) -> bool:
        return (
            isinstance(model_instance_field_value, DeclarativeBase) or
            isinstance(model_instance_field_value, list)
        )

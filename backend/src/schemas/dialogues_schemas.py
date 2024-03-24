import datetime

from pydantic import BaseModel, field_validator

from src.enums import TriggerEventType
from src.schemas.blocks_schemas import UnionBlockReadSchema
from src.utils import blocks_utils


class DialogueCreateSchema(BaseModel):
    trigger: 'TriggerCreateSchema'


class DialogueReadSchema(BaseModel):
    dialogue_id: int
    trigger: 'TriggerReadSchema'
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class TriggerCreateSchema(BaseModel):
    event_type: TriggerEventType
    value: str


class TriggerUpdateSchema(TriggerCreateSchema):
    pass


class TriggerReadSchema(BaseModel):
    trigger_id: int
    event_type: TriggerEventType
    value: str

    class Config:
        from_attributes = True


class DialogueWithBlocksReadSchema(DialogueReadSchema):
    blocks: list[UnionBlockReadSchema]

    @field_validator('blocks')
    @classmethod
    def transform_blocks(cls, blocks_to_transform):
        return [blocks_utils.validate_block_from_db(block) for block in blocks_to_transform]

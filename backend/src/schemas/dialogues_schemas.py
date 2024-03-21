import datetime

from pydantic import BaseModel, Field

from src.enums import TriggerEventType
from src.schemas.blocks_schemas import UnionBlockReadSchema


class DialogueCreateSchema(BaseModel):
    trigger: 'TriggerCreateSchema'


class DialogueReadSchema(BaseModel):
    dialogue_id: int
    trigger: 'TriggerReadSchema'
    created_at: datetime.datetime


class TriggerCreateSchema(BaseModel):
    event_type: TriggerEventType
    value: str


class TriggerReadSchema(BaseModel):
    trigger_id: int
    event_type: TriggerEventType
    value: str

    class Config:
        from_attributes = True


class DialogueReadSchemaWithBlocks(DialogueReadSchema):
    blocks: list[UnionBlockReadSchema]


class DialogueToCodeSchema(DialogueReadSchemaWithBlocks):
    has_states: bool = Field(default=False)

    class Config:
        from_attributes = True


class StateSchema(BaseModel):
    name: str


class StatesGroupSchema(BaseModel):
    name: str
    states: list[StateSchema] = Field(default_factory=list)

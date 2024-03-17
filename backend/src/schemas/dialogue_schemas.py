import datetime

from pydantic import BaseModel

from src.models import TriggerEventType


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

import datetime

from pydantic import BaseModel, Field

from src.schemas.dialogue_schemas import DialogueReadSchema


class ProjectReadSchema(BaseModel):
    project_id: int
    name: str
    created_at: datetime.datetime
    dialogues: list[DialogueReadSchema] = Field(default_factory=list)


class ProjectCreateSchema(BaseModel):
    name: str


class ProjectUpdateSchema(BaseModel):
    name: str

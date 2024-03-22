import datetime

from pydantic import BaseModel, Field

from src.schemas.dialogues_schemas import DialogueWithoutBlocksReadSchema


class ProjectReadSchema(BaseModel):
    project_id: int
    name: str
    user_id: int
    created_at: datetime.datetime
    dialogues: list[DialogueWithoutBlocksReadSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class ProjectCreateSchema(BaseModel):
    name: str


class ProjectUpdateSchema(BaseModel):
    name: str

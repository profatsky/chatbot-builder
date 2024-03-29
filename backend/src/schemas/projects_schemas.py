import datetime

from pydantic import BaseModel, Field

from src.enums import KeyboardType
from src.schemas.dialogues_schemas import DialogueReadSchema, DialogueWithBlocksReadSchema
from src.schemas.plugins_schemas import PluginReadSchema


class ProjectReadSchema(BaseModel):
    project_id: int
    name: str = Field(min_length=1, max_length=256)
    user_id: int
    start_message: str = Field(min_length=1, max_length=4098)
    start_keyboard_type: KeyboardType
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class ProjectWithPluginsReadSchema(ProjectReadSchema):
    plugins: list[PluginReadSchema] = Field(default_factory=list)


class ProjectWithDialoguesReadSchema(ProjectReadSchema):
    dialogues: list[DialogueReadSchema] = Field(default_factory=list)


class ProjectWithDialoguesAndBlocksReadSchema(ProjectWithDialoguesReadSchema):
    dialogues: list[DialogueWithBlocksReadSchema] = Field(default_factory=list)


class ProjectCreateSchema(BaseModel):
    name: str
    start_message: str = Field(min_length=1, max_length=4098)
    start_keyboard_type: KeyboardType


class ProjectUpdateSchema(BaseModel):
    name: str
    start_message: str = Field(min_length=1, max_length=4098)
    start_keyboard_type: KeyboardType

import datetime

from pydantic import BaseModel


class ProjectReadSchema(BaseModel):
    project_id: int
    name: str
    created_at: datetime.datetime


class ProjectCreateSchema(BaseModel):
    name: str


class ProjectUpdateSchema(BaseModel):
    name: str

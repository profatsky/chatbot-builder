import datetime

from pydantic import BaseModel


class DialogueTemplateReadSchema(BaseModel):
    template_id: int
    name: str
    summary: str
    description: str
    image_path: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

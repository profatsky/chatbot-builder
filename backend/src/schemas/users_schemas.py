import datetime

from pydantic import BaseModel, EmailStr


class UserReadSchema(BaseModel):
    user_id: int
    email: EmailStr
    registered_at: datetime.datetime
    is_verified: bool
    is_superuser: bool

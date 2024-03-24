from typing import Optional

from pydantic import BaseModel, Field

from src.enums import HandlerType


class StateSchema(BaseModel):
    name: str


class StatesGroupSchema(BaseModel):
    name: str
    states: list[StateSchema] = Field(default_factory=list)


class HandlerSchema(BaseModel):
    type: HandlerType = Field(default=HandlerType.MESSAGE)
    decorator: Optional[str] = None
    signature: Optional[str] = None
    body: list[str] = Field(default_factory=list)

    def add_to_body(self, code: str):
        self.body.append(code.strip())


class KeyboardSchema(BaseModel):
    declaration: str = None
    buttons: list[str] = Field(default_factory=list)

    def add_to_buttons(self, code: str):
        self.buttons.append(code)

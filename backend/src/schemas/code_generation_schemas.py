import re
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
        code = self._process_user_answers_in_code(code)
        self.body.append(code.strip())

    @staticmethod
    def _process_user_answers_in_code(code: str):
        pattern = r"answers\[(\d+)\]"

        match = re.search(pattern, code)
        if match:
            start_index = match.start()
            quote_index = code.rfind('"', 0, start_index)

            while quote_index != 0 and code[quote_index - 1] == '\\':
                quote_index = code.rfind('"', 0, quote_index - 1)

            code = code[:quote_index] + 'f' + code[quote_index:]

        def replace_match(match):
            return "{answers['answer" + match.group(1) + "']}"

        result = re.sub(pattern, replace_match, code)

        return result


class KeyboardSchema(BaseModel):
    declaration: str = None
    buttons: list[str] = Field(default_factory=list)

    def add_to_buttons(self, code: str):
        self.buttons.append(code)

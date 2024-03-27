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
        code = code.replace('\'', '"')
        pattern = r"answers\[(\d+)\]"

        search_from = 0
        while match := re.search(pattern, code[search_from:]):
            quote_index = code.rfind('"', 0, match.start() + search_from)
            if quote_index != -1 and code[quote_index - 1] != 'f':
                code = code[:quote_index] + 'f' + code[quote_index:]
                search_from += 1

            search_from += match.end()

        def replace_match(match):
            return "{answers['answer" + match.group(1) + "']}"

        result = re.sub(pattern, replace_match, code)

        return result


class KeyboardSchema(BaseModel):
    declaration: str = None
    buttons: list[str] = Field(default_factory=list)

    def add_to_buttons(self, code: str):
        self.buttons.append(code)

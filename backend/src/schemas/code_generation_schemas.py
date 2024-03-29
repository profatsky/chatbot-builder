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
        code = code.replace('\'', '"')
        code = self._process_access_to_user_answers_in_code(code)
        code = self._process_access_to_api_response_in_code(code)
        self.body.append(code.strip())

    def _process_access_to_user_answers_in_code(self, code: str):
        pattern = r'answers\[(\d+)\]'

        code = self._format_string_if_pattern_found(pattern, code)

        def replace_match(match):
            return "{answers['answer" + match.group(1) + "']}"

        result = re.sub(pattern, replace_match, code)

        return result

    def _process_access_to_api_response_in_code(self, code: str):
        pattern = r'response_data\["([a-zA-Z0-9_-]+)"\]'

        code = self._format_string_if_pattern_found(pattern, code)

        def replace_match(match):
            return "{response_data.get('" + match.group(1) + "')}"

        result = re.sub(pattern, replace_match, code)

        return result

    @staticmethod
    def _format_string_if_pattern_found(pattern, code):
        search_from = 0
        while match := re.search(pattern, code[search_from:]):
            quote_index = code.rfind('"', 0, match.start() + search_from)
            if quote_index != -1 and code[quote_index - 1] != 'f':
                code = code[:quote_index] + 'f' + code[quote_index:]
                search_from += 1

            search_from += match.end()

        return code


class KeyboardSchema(BaseModel):
    declaration: str = None
    buttons: list[str] = Field(default_factory=list)

    def add_to_buttons(self, code: str):
        self.buttons.append(code)

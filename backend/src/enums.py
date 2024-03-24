import enum


class KeyboardType(enum.Enum):
    INLINE_KEYBOARD = 'inline_keyboard'
    REPLY_KEYBOARD = 'reply_keyboard'


class HandlerType(enum.Enum):
    CALLBACK = 'callback'
    MESSAGE = 'message'


class TriggerEventType(enum.Enum):
    TEXT = 'text'
    COMMAND = 'command'
    BUTTON = 'button'


class BlockType(enum.Enum):
    TEXT_BLOCK = 'text_block'
    IMAGE_BLOCK = 'image_block'
    QUESTION_BLOCK = 'question_block'
    EMAIL_BLOCK = 'email_block'
    CSV_BLOCK = 'csv_block'
    API_BLOCK = 'api_block'


class AnswerMessageType(enum.Enum):
    ANY = 'any'
    TEXT = 'text'
    INT = 'int'
    EMAIL = 'email'
    PHONE_NUMBER = 'phone_number'


class HTTPMethod(enum.Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    CONNECT = 'CONNECT'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'

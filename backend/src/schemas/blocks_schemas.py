from typing import Union, Literal, Annotated

from pydantic import BaseModel, Field, HttpUrl, field_serializer

from src.enums import BlockType, AnswerMessageType, HTTPMethod


class BlockReadSchema(BaseModel):
    block_id: int
    sequence_number: int

    class Config:
        from_attributes = True


class BlockCreateSchema(BaseModel):
    sequence_number: int = Field(ge=1)


# Text block
class TextBlockReadSchema(BlockReadSchema):
    message_text: str = Field(min_length=1, max_length=4096)
    type: Literal[BlockType.TEXT_BLOCK.value]


class TextBlockCreateSchema(BlockCreateSchema):
    message_text: str = Field(min_length=1, max_length=4096)
    type: Literal[BlockType.TEXT_BLOCK.value]


# Image block
class ImageBlockReadSchema(BlockReadSchema):
    image_path: str = Field(min_length=1, max_length=256)
    type: Literal[BlockType.IMAGE_BLOCK.value]


class ImageBlockCreateSchema(BlockCreateSchema):
    image_path: str = Field(min_length=1, max_length=256)
    type: Literal[BlockType.IMAGE_BLOCK.value]


# Question block
class QuestionBlockReadSchema(BlockReadSchema):
    message_text: str = Field(min_length=1, max_length=4096)
    answer_type: AnswerMessageType
    type: Literal[BlockType.QUESTION_BLOCK.value]


class QuestionBlockCreateSchema(BlockCreateSchema):
    message_text: str = Field(min_length=1, max_length=4096)
    answer_type: AnswerMessageType
    type: Literal[BlockType.QUESTION_BLOCK.value]


# Email block
class EmailBlockReadSchema(BlockReadSchema):
    subject: str = Field(min_length=1, max_length=128)
    text: str = Field(min_length=1, max_length=8192)
    recipient_email: str = Field(min_length=6, max_length=254)
    type: Literal[BlockType.EMAIL_BLOCK.value]


class EmailBlockCreateSchema(BlockCreateSchema):
    subject: str = Field(min_length=1, max_length=128)
    text: str = Field(min_length=1, max_length=8192)
    recipient_email: str = Field(min_length=6, max_length=254)
    type: Literal[BlockType.EMAIL_BLOCK.value]


# CSV block
class CSVBlockReadSchema(BlockReadSchema):
    file_path: str = Field(min_length=1, max_length=256)
    data: dict
    type: Literal[BlockType.CSV_BLOCK.value]


class CSVBlockCreateSchema(BlockCreateSchema):
    file_path: str = Field(min_length=1, max_length=256)
    data: dict
    type: Literal[BlockType.CSV_BLOCK.value]


# API block
class APIBlockReadSchema(BlockReadSchema):
    url: HttpUrl
    http_method: HTTPMethod
    headers: dict
    body: dict
    type: Literal[BlockType.API_BLOCK.value]


class APIBlockCreateSchema(BlockCreateSchema):
    url: HttpUrl
    http_method: HTTPMethod
    headers: dict
    body: dict
    type: Literal[BlockType.API_BLOCK.value]

    @field_serializer('url')
    def serialize_url(self, url: HttpUrl):
        return str(url)


UnionBlockReadSchema = Annotated[
    Union[
        TextBlockReadSchema,
        ImageBlockReadSchema,
        QuestionBlockReadSchema,
        EmailBlockReadSchema,
        CSVBlockReadSchema,
        APIBlockReadSchema,
    ],
    Field(discriminator='type')
]
UnionBlockCreateSchema = Annotated[
    Union[
        TextBlockCreateSchema,
        ImageBlockCreateSchema,
        QuestionBlockCreateSchema,
        EmailBlockCreateSchema,
        CSVBlockCreateSchema,
        APIBlockCreateSchema,
    ],
    Field(discriminator='type')
]

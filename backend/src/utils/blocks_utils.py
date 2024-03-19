from typing import Type, Union

from src.enums import BlockType
from src.models import (
    TextBlockModel,
    ImageBlockModel,
    QuestionBlockModel,
    EmailBlockModel,
    CSVBlockModel,
    APIBlockModel
)

BlockModel = Type[
    Union[
        TextBlockModel,
        ImageBlockModel,
        QuestionBlockModel,
        EmailBlockModel,
        CSVBlockModel,
    ]
]


def get_block_model_by_type(block_type: BlockType) -> BlockModel:
    types_to_blocks = {
        BlockType.TEXT_BLOCK.value: TextBlockModel,
        BlockType.IMAGE_BLOCK.value: ImageBlockModel,
        BlockType.QUESTION_BLOCK.value: QuestionBlockModel,
        BlockType.EMAIL_BLOCK.value: EmailBlockModel,
        BlockType.CSV_BLOCK.value: CSVBlockModel,
        BlockType.API_BLOCK.value: APIBlockModel,
    }

    return types_to_blocks[block_type]

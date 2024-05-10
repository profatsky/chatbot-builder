import asyncio

from src.core.db import async_session_maker
from src.enums import TriggerEventType, AnswerMessageType
from src.models.dialogues import DialogueModel, TriggerModel
from src.models.blocks import TextBlockModel, QuestionBlockModel, CSVBlockModel
from src.models.dialogue_templates import DialogueTemplateModel


async def create_survey_dialogue_template():
    async with async_session_maker() as session:
        trigger = TriggerModel(
            event_type=TriggerEventType.TEXT,
            value='Опрос'
        )

        dialogue = DialogueModel(
            trigger=trigger
        )

        blocks = [
            TextBlockModel(
                sequence_number=1,
                message_text='Пройдите опрос',
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=2,
                message_text='Как вас зовут?',
                answer_type=AnswerMessageType.TEXT,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=3,
                message_text='Сколько вам лет?',
                answer_type=AnswerMessageType.INT,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=4,
                message_text='Кем вы работаете?',
                answer_type=AnswerMessageType.TEXT,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=5,
                message_text='Введите свой номер телефона',
                answer_type=AnswerMessageType.PHONE_NUMBER,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=6,
                message_text='Введите свою электронную почту',
                answer_type=AnswerMessageType.EMAIL,
                dialogue=dialogue,
            ),
            CSVBlockModel(
                sequence_number=7,
                file_path='survey.csv',
                data={
                    'age': 'answers[2]',
                    'job': 'answers[3]',
                    'name': 'answers[1]',
                    'email': 'answers[5]',
                    'phone_number': 'answers[4]'
                },
                dialogue=dialogue,
            ),
            TextBlockModel(
                sequence_number=8,
                message_text='Благодарим за участие в опросе!',
                dialogue=dialogue,
            ),
        ]

        template = DialogueTemplateModel(
            name='Опрос',
            summary='Сбор данных от пользователя посредством опроса',
            description='Шаблон опроса пользователей чат-бота для сбора следующей информации: имя, возраст, '
                        'род деятельности, номер телефона и электронная почта. Введенные пользователем данные будут '
                        'сохранены в csv-файл.',
            dialogue=dialogue,
            image_path='dialogue_templates/survey.png',
        )

        session.add(trigger)
        session.add(dialogue)
        for block in blocks:
            session.add(block)
        session.add(template)

        await session.commit()


if __name__ == '__main__':
    asyncio.run(create_survey_dialogue_template())

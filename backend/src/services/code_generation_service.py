from jinja2 import Template, Environment, FileSystemLoader
from sqlalchemy.ext.asyncio import AsyncSession

from src.enums import KeyboardType, HandlerType
from src.schemas.code_generation_schemas import HandlerSchema, StateSchema, StatesGroupSchema, KeyboardSchema
from src.schemas.projects_schemas import ProjectWithDialoguesAndBlocksReadSchema
from src.services import projects_service
from src.services.exceptions.dialogues_exceptions import NoDialoguesInProject
from src.templates import code


async def get_bot_code(
        user_id: int,
        project_id: int,
        session: AsyncSession,
) -> str:
    project = await projects_service.check_access_and_get_project_with_dialogues_and_blocks(
        user_id=user_id,
        project_id=project_id,
        session=session,
    )

    if not project.dialogues:
        raise NoDialoguesInProject

    bot_code = _generate_bot_code(project)
    return bot_code


# TODO refactoring
# TODO add customize env variables
# TODO changed start func call
def _generate_bot_code(project: ProjectWithDialoguesAndBlocksReadSchema) -> str:
    utils_funcs = set()
    states_groups: list[StatesGroupSchema] = []
    handlers: list[HandlerSchema] = []
    commands_values: list[str] = []

    start_keyboard = _get_start_keyboard(project.start_keyboard_type)

    for dialogue in project.dialogues:

        states_group = None

        handler = HandlerSchema()
        handler.signature = code.func_signature_for_common_handler_with_msg.format(
            trigger_event_type=dialogue.trigger.event_type.value,
            dialogue_id=dialogue.dialogue_id,
        )

        if dialogue.trigger.event_type.value == 'command':
            commands_values.append(dialogue.trigger.value)
            handler.decorator = code.command_decorator.format(trigger_value=dialogue.trigger.value)

        elif dialogue.trigger.event_type.value == 'button':
            if project.start_keyboard_type == KeyboardType.INLINE_KEYBOARD:
                start_keyboard.add_to_buttons(
                    code.inline_keyboard_button.format(text=dialogue.trigger.value)
                )
                handler.decorator = code.callback_button_decorator.format(trigger_value=dialogue.trigger.value)
                handler.signature = code.func_signature_for_callback_handler_with_callback.format(
                    trigger_event_type=dialogue.trigger.event_type.value,
                    dialogue_id=dialogue.dialogue_id,
                )
                handler.type = HandlerType.CALLBACK
                handler.add_to_body(code.callback_answer)
            else:
                start_keyboard.add_to_buttons(
                    code.reply_keyboard_button.format(text=dialogue.trigger.value)
                )
                handler.decorator = code.text_button_decorator.format(trigger_value=dialogue.trigger.value)

        elif dialogue.trigger.event_type.value == 'text':
            handler.decorator = code.text_decorator.format(trigger_value=dialogue.trigger.value)

        if not dialogue.blocks:
            handler.add_to_body('pass')

        for block in dialogue.blocks:
            if block.type == 'text_block':
                if handler.type == HandlerType.CALLBACK:
                    handler.add_to_body(code.callback_message_answer.format(message_text=block.message_text))
                elif handler.type == HandlerType.MESSAGE:
                    handler.add_to_body(code.message_answer.format(message_text=block.message_text))

            elif block.type == 'image_block':
                if handler.type == HandlerType.CALLBACK:
                    handler.add_to_body(code.callback_image_block.format(image_path=block.image_path))
                elif handler.type == HandlerType.MESSAGE:
                    handler.add_to_body(code.image_block.format(image_path=block.image_path))

            elif block.type == 'question_block':
                if states_group is None:
                    state = StateSchema(name=f'state_from_block{block.sequence_number}')
                    states_group = StatesGroupSchema(
                        name=f'StatesGroup{len(states_groups) + 1}',
                        states=[state]
                    )
                    states_groups.append(states_group)

                    if handler.type == HandlerType.CALLBACK:
                        handler.add_to_body(
                            code.callback_message_answer_with_reply_kb_remove.format(message_text=block.message_text)
                        )
                    elif handler.type == HandlerType.MESSAGE:
                        handler.add_to_body(
                            code.message_answer_with_reply_kb_remove.format(message_text=block.message_text)
                        )

                    handler.add_to_body(
                        code.set_state.format(states_group_name=states_group.name, state_name=state.name)
                    )

                    if handler.type == HandlerType.CALLBACK:
                        handler.signature = code.func_signature_for_callback_handler_with_callback_and_state.format(
                            trigger_event_type=dialogue.trigger.event_type.value,
                            dialogue_id=dialogue.dialogue_id,
                        )
                    elif handler.type == HandlerType.MESSAGE:
                        handler.signature = code.func_signature_for_common_handler_with_msg_and_state.format(
                            trigger_event_type=dialogue.trigger.event_type.value,
                            dialogue_id=dialogue.dialogue_id,
                        )

                    handlers.append(handler)
                else:
                    state = StateSchema(name=f'state_from_block{block.sequence_number}')
                    states_groups[-1].states.append(state)

                    handler.add_to_body(
                        code.message_answer_with_reply_kb_remove.format(message_text=block.message_text)
                    )
                    handler.add_to_body(
                        code.set_state.format(states_group_name=states_group.name, state_name=state.name)
                    )
                    handlers.append(handler)

                handler = HandlerSchema()
                handler.decorator = code.state_decorator.format(
                    states_group_name=states_group.name,
                    state_name=state.name,
                )
                handler.signature = code.func_signature_for_state_handler_with_msg_and_state.format(
                    state_name=state.name,
                    dialogue_id=dialogue.dialogue_id,
                )

                if block.answer_type.value == 'text':
                    handler.add_to_body(code.answer_text_type_check)

                elif block.answer_type.value == 'int':
                    handler.add_to_body(code.answer_int_type_check)

                elif block.answer_type.value == 'email':
                    handler.add_to_body(code.answer_email_type_check)

                    utils_funcs.add(code.is_email.strip())

                elif block.answer_type.value == 'phone_number':
                    handler.add_to_body(code.answer_phone_number_type_check)

                    utils_funcs.add(code.is_phone_number.strip())

                handler.add_to_body(code.update_state.format(answer_num=len(states_group.states)))

            elif block.type == 'email_block':
                handler.add_to_body(
                    code.email_block.format(
                        recipient_email=block.recipient_email,
                        subject=block.subject,
                        text=block.text,
                    )
                )

                utils_funcs.add(code.send_email.strip())
                utils_funcs.add(code.is_answer_from_user.strip())

        if states_group:
            handler.add_to_body(code.clear_state)
            handler.add_to_body(code.call_start_func)
        handlers.append(handler)

    if not start_keyboard.buttons:
        start_keyboard = None

    template = _get_bot_template()
    bot_code = template.render({
        'utils_funcs': utils_funcs,
        'states_groups': states_groups,
        'handlers': handlers,
        'commands_values': commands_values,
        'start_keyboard': start_keyboard,
        'start_message': project.start_message,
    })
    return bot_code


def _get_start_keyboard(keyboard_type: KeyboardType) -> KeyboardSchema:
    start_keyboard = KeyboardSchema()
    if keyboard_type == KeyboardType.INLINE_KEYBOARD:
        start_keyboard.declaration = code.inline_keyboard_declaration
    else:
        start_keyboard.declaration = code.reply_keyboard_declaration
    return start_keyboard


def _get_bot_template() -> Template:
    with open('src/templates/bot_template.py.j2', 'r', encoding='utf-8') as f:
        template_str = f.read()

    env = Environment(
        loader=FileSystemLoader('src/templates/'),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.from_string(template_str)
    return template

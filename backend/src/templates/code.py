# decorators
command_decorator = '@dp.message(filters.StateFilter(None), filters.Command("{trigger_value}"))'
button_decorator = '@dp.message(filters.StateFilter(None), F.text == "{trigger_value}")'
text_decorator = '@dp.message(filters.StateFilter(None), F.text == "{trigger_value}")'
state_decorator = '@dp.message(filters.StateFilter({states_group_name}.{state_name}))'

# funcs signatures
func_signature_for_common_handler_with_msg = (
    'async def handler_{trigger_event_type}_dialogue{dialogue_id}(message: types.Message):'
)
func_signature_for_common_handler_with_msg_and_state = (
    'async def handler_{trigger_event_type}_dialogue{dialogue_id}(message: types.Message, state: FSMContext):'
)
func_signature_for_state_handler_with_msg_and_state = (
    'async def handler_{state_name}_dialogue{dialogue_id}(message: types.Message, state: FSMContext):'
)

# blocks
text_block_code = 'await message.answer("{message_text}")'

image_block = '''
    # Отправка изображения
    try:
        image = types.FSInputFile("{image_path}")
        await message.answer_photo(image)
    except Exception as e:
        logging.info(f"Ошибка при отправке изображения {image_path}: {{e}}")
'''

text_block_code_with_reply_kb_remove = (
    'await message.answer("{message_text}", reply_markup=types.ReplyKeyboardRemove())'
)

email_block = '''
    # Отправка Email
    recipient_email = "{recipient_email}"
    if is_answer_from_user(recipient_email):
        recipient_email = (await state.get_data()).get(recipient_email)
    try:
        await send_email(
            title="{subject}",
            content="{text}",
            recipient_email=recipient_email
        )
    except Exception as e:
        logging.info(f'Ошибка при отправке письма на email {{recipient_email}}: {{e}}')
'''

set_state = 'await state.set_state({states_group_name}.{state_name})'
update_state = 'await state.update_data(answer{answer_num}=message.text)'
clear_state = 'await state.clear()'

call_start_func = 'await handler_command_start(message)'

# answers type check
answer_text_type_check = '''
    if not isinstance(message.text, str):
        return await message.answer("Неверный тип сообщения! Необходимо ввести текст!")
'''

answer_int_type_check = '''
    if not message.text.isdigit():
        return await message.answer("Неверный тип сообщения! Необходимо ввести целое число!")
'''

answer_email_type_check = '''
    if not is_email(message.text):
        return await message.answer("Неверный тип сообщения! Необходимо ввести email!")
'''

answer_phone_number_type_check = '''
    if not is_phone_number(message.text):
        return await message.answer("Неверный тип сообщения! Необходимо ввести номер телефона!")
'''

# funcs
is_email = '''
def is_email(string: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.fullmatch(pattern, string))
'''

is_phone_number = '''
def is_phone_number(string: str) -> bool:
    pattern = r'^8[0-9]{10}$'
    return bool(re.fullmatch(pattern, string))
'''

send_email = '''
async def send_email(title: str, content: str, recipient_email: str):
    smtp = SMTP(
        hostname=EMAIL_HOST,
        port=EMAIL_PORT,
        start_tls=False,
        use_tls=False,
    )
    await smtp.connect()
    await smtp.starttls()
    await smtp.login(EMAIL_HOST_USER, EMAIL_GOOGLE_APP_PASSWORD)

    message = EmailMessage()
    message['From'] = EMAIL_HOST_USER
    message['To'] = recipient_email
    message['Subject'] = title
    message.set_content(content)

    await smtp.send_message(message)
    await smtp.quit()
'''

is_answer_from_user = '''
def is_answer_from_user(string: str) -> bool:
    pattern = r'^answer\[\d+\]$'
    return bool(re.fullmatch(pattern, string))
'''
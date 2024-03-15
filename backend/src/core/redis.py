# TODO replace with redis
from pydantic import EmailStr

user_ids_to_email_verification_codes: dict[int, int] = {}
user_ids_to_email_and_change_verification_codes: dict[int, tuple[int, EmailStr]] = {}

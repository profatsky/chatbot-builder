import os

from dotenv import load_dotenv
from fastapi_users.authentication import CookieTransport

load_dotenv()

DEBUG = os.getenv('DEBUG')

# Database
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

# Auth
TRANSPORT = CookieTransport(cookie_name='auth', cookie_max_age=36000)
SECRET = os.environ.get('SECRET')

# Email sender
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_GOOGLE_APP_PASSWORD = os.environ.get('EMAIL_GOOGLE_APP_PASSWORD')

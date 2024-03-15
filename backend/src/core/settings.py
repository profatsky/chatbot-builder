import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get('DEBUG')

BASE_URL = os.environ.get('BASE_URL')

JWT_SECRET = os.environ.get('JWT_SECRET')

# Database
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

# Email sender
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_GOOGLE_APP_PASSWORD = os.environ.get('EMAIL_GOOGLE_APP_PASSWORD')

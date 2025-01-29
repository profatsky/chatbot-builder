import os

from dotenv import load_dotenv

load_dotenv()

CLIENT_APP_URL = os.environ.get('CLIENT_APP_URL')

JWT_SECRET = os.environ.get('JWT_SECRET')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
TEST_DB_NAME = os.environ.get('TEST_DB_NAME')

import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "").split(",")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

INITIAL_ADMIN_NAME = os.environ.get("INITIAL_ADMIN_NAME")
INITIAL_ADMIN_PASS = os.environ.get("INITIAL_ADMIN_PASS")

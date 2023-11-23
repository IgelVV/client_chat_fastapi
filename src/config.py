import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_KEY = "82dd23058649a21028c23ed4d4c819f7c86afaeea530356da4d92807e8fc3ffc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

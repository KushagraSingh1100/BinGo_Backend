import os
from dotenv import load_dotenv

ENVIRONMENT = os.getenv("FASTAPI_ENV", "development")

dotenv_path = f".env.{ENVIRONMENT}"
load_dotenv(dotenv_path)

API_TOKEN = os.getenv("TEMP_TOKEN")


def verify_token(token: str) -> bool:
    return token == API_TOKEN

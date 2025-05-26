import os
import logging
import sys
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

REQUIRED_ENV_VARS = [
    'AUTH_EMAIL',
    'AUTH_PASSWORD',
    'USER_FIRST_NAME',
    'USER_LAST_NAME',
    'USER_BIRTHDAY',
    'USER_PASSPORT_NUMBER',
    'USER_EXPIRE_DATA',
    'USER_PHONE_HEADER',
    'USER_PHONE_BODY',
    'USER_ADDRESS_LINE',
    'DEFAULT_APPLYING_FROM',
    'DEFAULT_GOING_TO',
    'PROXY'
]

def validate_env_vars():
    missing_vars = [var for var in REQUIRED_ENV_VARS if os.getenv(var) is None]
    if missing_vars:
        raise EnvironmentError(f"Missing environment variables: {missing_vars}")

AUTH_EMAIL = os.getenv("AUTH_EMAIL")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")

USER_FIRST_NAME = os.getenv("USER_FIRST_NAME")
USER_LAST_NAME = os.getenv("USER_LAST_NAME")
USER_BIRTHDAY = os.getenv("USER_BIRTHDAY")
USER_PASSPORT_NUMBER = os.getenv("USER_PASSPORT_NUMBER")
USER_EXPIRE_DATA = os.getenv("USER_EXPIRE_DATA")
USER_PHONE_HEADER = os.getenv("USER_PHONE_HEADER")
USER_PHONE_BODY = os.getenv("USER_PHONE_BODY")
USER_ADDRESS_LINE = os.getenv("USER_ADDRESS_LINE")

DEFAULT_APPLYING_FROM = os.getenv("DEFAULT_APPLYING_FROM")
DEFAULT_GOING_TO = os.getenv("DEFAULT_GOING_TO")
PROXY = os.getenv("PROXY")

LOGIN_URL = 'https://visa.vfsglobal.com/usa/en/aut/login' 
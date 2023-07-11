import os
from typing import Set

from dotenv import load_dotenv

load_dotenv("../.env")


class Config:
    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]

    TELEGRAM_BOT_API_KEY: str = os.environ["TELEGRAM_BOT_API_KEY"]
    TELEGRAM_BOT_APARTMENTS_GROUP_CHAT_ID: str = os.environ[
        "TELEGRAM_BOT_APARTMENTS_GROUP_CHAT_ID"
    ]
    TELEGRAM_BOT_APARTMENTS_LOGS_GROUP_CHAT_ID: str = os.environ[
        "TELEGRAM_BOT_APARTMENTS_LOGS_GROUP_CHAT_ID"
    ]

    FACEBOOK_USERNAME: str = os.environ["FACEBOOK_USERNAME"]
    FACEBOOK_PASSWORD: str = os.environ["FACEBOOK_PASSWORD"]
    FACEBOOK_GROUPS: Set[str] = {
        v.strip() for v in os.environ["FACEBOOK_GROUPS"].split(",") if v
    }

    MAX_TEXT_LEN: int = 600
    MAX_HOURS_DIFFERENCE: int = 3

    MAX_POSTS_TO_ENRICH_IN_RUN = 20


config = Config()

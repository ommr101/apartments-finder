from typing import List

from dotenv import dotenv_values

env_vars = dotenv_values("../.env")


class Config:
    OPENAI_API_KEY: str = env_vars["OPENAI_API_KEY"]

    TELEGRAM_BOT_API_KEY: str = env_vars["TELEGRAM_BOT_API_KEY"]
    TELEGRAM_BOT_APARTMENTS_GROUP_CHAT_ID: str = env_vars[
        "TELEGRAM_BOT_APARTMENTS_GROUP_CHAT_ID"
    ]
    TELEGRAM_BOT_APARTMENTS_LOGS_GROUP_CHAT_ID: str = env_vars[
        "TELEGRAM_BOT_APARTMENTS_LOGS_GROUP_CHAT_ID"
    ]

    FACEBOOK_USERNAME: str = env_vars["FACEBOOK_USERNAME"]
    FACEBOOK_PASSWORD: str = env_vars["FACEBOOK_PASSWORD"]
    FACEBOOK_GROUPS: List[str] = [
        v.strip() for v in env_vars["FACEBOOK_GROUPS"].split(",") if v
    ]

    MAX_TEXT_LEN: int = 600
    MAX_HOURS_DIFFERENCE: int = 4


config = Config()

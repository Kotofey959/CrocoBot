from dataclasses import dataclass

from environs import Env

env = Env()
env.read_env()

CRM_API_KEY = env('CRM_API_KEY')
PAYMENTS_TOKEN = env('PAYMENTS_TOKEN')

PHONE_REG = '^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
USER_NAME_REG = '^[А-ЯЁ][а-яё]* [А-ЯЁ][а-яё]*$'


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))

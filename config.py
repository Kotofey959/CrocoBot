from dataclasses import dataclass

from environs import Env

CRM_API_KEY = "11b1abf2e30a8a5286cd49a7918aaafccc305096"

PHONE_REG = '^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
USER_NAME_REG = '^[А-ЯЁ][а-яё]* [А-ЯЁ][а-яё]*$'

PAYMENTS_TOKEN = '381764678:TEST:51451'


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))

from typing import Text

from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


from api.query import get_products_in_group, get_groups_list


def category_kb(msg):
    builder = ReplyKeyboardBuilder()
    groups = get_groups_list()
    for group in groups:
        if group['pathName'].endswith(msg):
            builder.add(types.KeyboardButton(text=group['name']))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def products_kb(msg):
    builder = ReplyKeyboardBuilder()
    products = get_products_in_group()
    for product in products:
        builder.add(types.KeyboardButton(text=f'{product["name"]}|{int(product["salePrices"][0]["value"] // 100)} руб'))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def main_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Техника'), types.KeyboardButton(text='Профиль'))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def order_kb(msg):
    builder = ReplyKeyboardBuilder()
    for prod in msg:
        builder.add(
            types.KeyboardButton(text=f'{prod.get("name")}|{int(prod.get("salePrices")[0].get("value") / 100)} руб')
        )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def share_phone():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Отправить номер телефона', request_contact=True))
    return builder.as_markup(resize_keyboard=True)


def custom_kb(*kwargs: Text):
    builder = ReplyKeyboardBuilder()
    for value in kwargs:
        builder.add(types.KeyboardButton(text=value))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

import requests
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from api.link import CRMLink
from config import CRM_API_KEY

headers = {
        'Authorization': CRM_API_KEY,
    }
response = requests.get(CRMLink().productfolder,
                        headers=headers).json()

categories_list = [category['name'] for category in response['rows']]


def category_kb(msg):
    response = requests.get(CRMLink().productfolder,
                            headers=headers).json()
    builder = ReplyKeyboardBuilder()
    groups = list(response['rows'])
    for group in groups:
        if group['pathName'].endswith(msg):
            builder.add(types.KeyboardButton(text=group['name']))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def products_kb(msg):
    builder = ReplyKeyboardBuilder()
    response = requests.get(f"{CRMLink().assortment}/?filter=pathname~{msg}", headers=headers).json()
    for product in response['rows']:
        builder.add(types.KeyboardButton(text=f'{product["name"]}|{int(product["salePrices"][0]["value"]//100)} руб'))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def main_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Техника'), types.KeyboardButton(text='Гыгык'))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

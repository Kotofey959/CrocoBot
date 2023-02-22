from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import requests

headers = {
        'Authorization': '11b1abf2e30a8a5286cd49a7918aaafccc305096',
    }
response = requests.get("https://online.moysklad.ru/api/remap/1.2/entity/productfolder",
                        headers=headers).json()

categories_list = [category['name'] for category in response['rows']]


def category_kb(msg):
    response = requests.get("https://online.moysklad.ru/api/remap/1.2/entity/productfolder",
                            headers=headers).json()
    builder = ReplyKeyboardBuilder()
    groups = [group for group in response['rows']]
    for group in groups:
        if group['pathName'].endswith(msg):
            builder.add(types.KeyboardButton(text=group['name']))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def products_kb(msg):
    builder = ReplyKeyboardBuilder()
    response = requests.get(f'https://online.moysklad.ru/api/remap/1.2/entity/assortment'
                            f'/?filter=pathname~{msg}',
                            headers=headers).json()
    for product in response['rows']:
        builder.add(types.KeyboardButton(text=f'{product["name"]}|{int(product["salePrices"][0]["value"]//100)} руб'))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def main_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Техника'), types.KeyboardButton(text='Гыгык'))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

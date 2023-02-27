from .link import CRMLink
from config import CRM_API_KEY
import requests
import json

get_headers = {
    'Authorization': CRM_API_KEY,
}


# Получения списка названий групп товаров
def get_groups_list():
    response = requests.get(CRMLink().productfolder, headers=get_headers).json()
    return list(response.get('rows'))


# Получения списка товаров в группе
def get_products_in_group(value: str):
    response = requests.get(f"{CRMLink().assortment}/?filter=pathname~{value}", headers=get_headers).json()
    return response.get("rows")


# Получение списка товаров в группе без остатков
def get_products_to_order(value: str):
    all_products = get_products_in_group(value)
    return [prod for prod in all_products if prod.get('stock') == 0]


# Получения прайса с остатками текстом
def get_price(value: str):
    products = get_products_in_group(value)
    price_list = [
        f"<b>{prod.get('name')}</b>\n<b>Цена</b> {int(prod.get('salePrices')[0].get('value') / 100)} <b>В наличии:</b>{int(prod.get('stock'))}"
        for prod in products]
    return "\n\n".join(price_list)

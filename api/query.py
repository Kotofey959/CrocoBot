from typing import List

from sqlalchemy import select

from db import User
from db.users import get_user
from helper import product_to_kwargs_by_link
from .headers import get_headers
from .link import CRMLink
from config import CRM_API_KEY
import requests
import json


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


# Получение позиций заказа
def get_positions(link) -> List:
    positions = requests.get(link, headers=get_headers).json()
    products = []
    for pos in positions.get("rows"):
        product_link = pos.get("assortment").get("meta").get("href")
        products.append(product_to_kwargs_by_link(product_link))
    return products


# Получение заказов пользователя в CRM текстом
async def get_user_orders(user_id, session_maker) -> List:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).filter_by(user_id=user_id))
            user: User = sql_res.scalar()
            all_orders = requests.get(CRMLink().customerorder, headers=get_headers).json()
            counter = 0
            user_orders = []
            for order in all_orders.get("rows"):
                if order.get("agent").get("meta").get("href") == user.crm_link:
                    counter += 1
                    product = get_positions(order.get("positions").get("meta").get("href"))[0]
                    order_status = requests.get(order.get("state").get("meta").get("href"), headers=get_headers).json()
                    user_orders.append(f'{counter})\n'
                                       f'Товар: {product.get("name")}\n'
                                       f'Цена: {product.get("price")}руб\n'
                                       f'Статус заказа: {order_status.get("name")}')
            return user_orders

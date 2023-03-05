"""
Всопомгательные методы.
"""

from typing import Dict, Optional

import requests

from config import CRM_API_KEY


get_headers = {
    'Authorization': CRM_API_KEY,
}


def parse_name_to_kwargs(raw_name: str) -> Dict:
    """
    Разбирает название на параметры продукта.

    :param raw_name: Название
    :return: Разобранное название.
    """
    name, price = raw_name.split('|')

    return {
        "price": _get_price_str(price),
        "raw_name": raw_name,
        "name": name,
        "model": None,
        "memory": None,
        "color": None,
        "currency": "руб"
    }


def _get_price_str(value: str) -> Optional[float]:
    price = None
    try:
        price = int(value.rstrip(' руб')) * 100
    except Exception as ex:
        print(f"Ты лох: {ex}")

    return price


def parse_product_to_kwargs(product_link) -> Dict:
    product = requests.get(product_link, headers=get_headers).json()
    return {
        "name": product.get("name"),
        "price": int(product.get("salePrices")[0].get("value") / 100),
    }

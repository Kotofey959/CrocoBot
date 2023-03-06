"""
Всопомгательные методы.
"""

from typing import Dict, Optional

import requests

from api.headers import get_headers


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


def product_to_kwargs_by_json(product_json) -> Dict:
    return {
        "name": product_json.get("name"),
        "price": int(product_json.get("salePrices")[0].get("value") / 100),
        "pathname": product_json.get("pathName"),
    }


def product_to_kwargs_by_link(product_link) -> Dict:
    product_json = requests.get(product_link, headers=get_headers).json()
    return product_to_kwargs_by_json(product_json)

"""
Всопомгательные методы.
"""

__author__ = "Maksimov A.V."

from typing import Dict, Optional


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
        price = float(value.rstrip(' руб')) * 100
    except Exception as ex:
        print(f"Ты лох: {ex}")

    return price

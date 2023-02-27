import json

import requests

from api.link import CRMLink
from config import CRM_API_KEY
from helper import parse_name_to_kwargs


async def get_product_data(product):
    parsed_product = parse_name_to_kwargs(product)
    headers = {
        'Authorization': CRM_API_KEY,
    }

    response = requests.get(
        f"{CRMLink().product}"
        f"?filter=name={parsed_product.get('name')}",
        headers=headers).json()
    product = None

    for prod in response.get('rows'):
        if prod.get('salePrices')[0].get('value') == parsed_product.get("price"):
            product = prod
            break

    product_data = {
        "quantity": 1,
        "price": parsed_product.get("price"),
        "discount": 0,
        "vat": 0,
        "assortment": {
            "meta": {
                "href": product.get("meta").get("href"),
                "type": "product",
                "mediaType": "application/json"
            }
        },
    }
    return product_data


async def create_order(product, user_link):
    headers = {
        'Authorization': CRM_API_KEY,
        'Content-Type': 'application/json',
    }
    product_data = get_product_data(product)
    data = {
        "organization": {
            "meta": {
                "href": "https://online.moysklad.ru/api/remap/1.2/entity/organization/0408863f-aaaf-11ed-0a80-0b5f0026616e",
                "type": "organization",
                "mediaType": "application/json"
            }
        },
        "agent": {
            "meta": {
                "href": user_link,
                "type": "counterparty",
                "mediaType": "application/json"
            }
        },
        "positions": [product_data]
    }

    requests.post('https://online.moysklad.ru/api/remap/1.2/entity/customerorder',
                  headers=headers,
                  data=json.dumps(data))

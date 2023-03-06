import json

import requests
from sqlalchemy import select

from api.headers import post_headers
from api.link import CRMLink
from config import CRM_API_KEY
from db import User
from helper import parse_name_to_kwargs


def get_product_data(product):
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


async def create_order(product, user_id, session_maker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).filter_by(user_id=user_id))
            user: User = sql_res.scalar()
            user_link = user.crm_link

    product_data = get_product_data(product)
    data = {
        "organization": {
            "meta": {
                "href": CRMLink().organization,
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

    requests.post(CRMLink().customerorder,
                  headers=post_headers,
                  data=json.dumps(data))

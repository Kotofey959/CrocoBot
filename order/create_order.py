import json

import requests


async def get_product_data(product):
    title, price = product.split('|')

    headers = {
        'Authorization': '11b1abf2e30a8a5286cd49a7918aaafccc305096',
    }

    response = requests.get(f"https://online.moysklad.ru/api/remap/1.2/entity/product/"
                            f"?filter=name={title}",
                            headers=headers).json()
    product = None
    for prod in response.get('rows'):
        if prod.get('salePrices')[0].get('value') == int(price.rstrip(' руб')) * 100:
            product = prod
            break

    product_data = {
        "quantity": 1,
        "price": float(price.rstrip(' руб')),
        "discount": 0,
        "vat": 0,
        "assortment": {
            "meta": {
                "href": product.get('meta').get('href'),
                "type": "product",
                "mediaType": "application/json"
            }
        },
    }
    return product_data


async def create_order(product, user_link):
    headers = {
        'Authorization': '11b1abf2e30a8a5286cd49a7918aaafccc305096',
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

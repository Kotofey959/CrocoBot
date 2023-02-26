import json

import requests

from config import CRM_API_KEY


async def register_user(name: str, phone_number: str):
    headers = {
        'Authorization': CRM_API_KEY,
        'Content-Type': 'application/json'
    }

    data = {
        "name": str(name),
        "phone": str(phone_number),
    }

    response = requests.post('https://online.moysklad.ru/api/remap/1.2/entity/counterparty',
                                   headers=headers,
                                   data=json.dumps(data)).json()

    return response.get('meta').get('href')

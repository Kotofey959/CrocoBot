import requests
import json


async def register_user(name, phone_number):
    headers = {
        'Authorization': '11b1abf2e30a8a5286cd49a7918aaafccc305096',
        'Content-Type': 'application/json'
    }

    data = {"name": f"{name}",
            "phone": f"{phone_number}",
            }

    response = requests.post('https://online.moysklad.ru/api/remap/1.2/entity/counterparty',
                                   headers=headers,
                                   data=json.dumps(data)).json()

    user_link = response.get('meta').get('href')

    return user_link

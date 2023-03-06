import requests

from api.headers import get_headers
from api.link import CRMLink
from config import CRM_API_KEY
from helper import product_to_kwargs_by_json

resp_groups = requests.get(CRMLink().productfolder, headers=get_headers).json()
product_groups = [prod.get("name") for prod in resp_groups.get("rows")]

resp_products = requests.get(CRMLink().product, headers=get_headers).json()
products_list = []
for prod in resp_products.get("rows"):
    product_data = product_to_kwargs_by_json(prod)
    if product_data.get("pathname").startswith("Техника"):
        products_list.append(f"{product_data.get('name')}|{product_data.get('price')} руб")



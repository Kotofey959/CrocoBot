from config import CRM_API_KEY

get_headers = {
    'Authorization': CRM_API_KEY,
}

post_headers = {
    'Authorization': CRM_API_KEY,
    'Content-Type': 'application/json',
}
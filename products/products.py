import gspread
from environs import Env

env = Env()
env.read_env()

gc = gspread.service_account(filename=env('PATH_JSON'))
sh = gc.open('Crocodiler')


async def get_products(category: str | None, worksheet: str) -> str:
    selected_worksheet = sh.worksheet(worksheet)
    list_products = selected_worksheet.get_all_records()
    list_show = []
    if category:
        for i in list_products:
            if category == i['Категория']:
                list_show.append(f'{i["Модель"]} {i["Цена"]}руб')
    else:
        for i in list_products:
            list_show.append(f'{i["Модель"]} {i["Цена"]}руб')
    return "\n".join(list_show)

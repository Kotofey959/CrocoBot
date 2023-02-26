"""
Работа со ссылками CRM.
"""


class CRMLink:

    def __init__(self):
        self.base_link = "https://online.moysklad.ru/api/remap/"
        self.api_version = "1.2"
        self.base_object = "entity"

        self._base_link = None

    @property
    def base_link(self):
        if self._base_link is None:
            self._base_link = [self.base_link, self.api_version, self.base_object].join("/")

        return self._base_link

    @property
    def productfolder(self):
        return f"{self.base_link}/productfolder"

    @property
    def assorment(self):
        return f"{self.base_link}/assortment"

    @property
    def product(self):
        return f"{self.base_link}/product"

    @property
    def counterparty(self):
        return f'{self.base_link}/counterparty'

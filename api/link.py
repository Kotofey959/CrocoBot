"""
Работа со ссылками CRM.
"""


class CRMLink:

    def __init__(self):
        self.link = "https://online.moysklad.ru/api/remap"
        self.api_version = "1.2"
        self.base_object = "entity"

        self._base_link = None

    @property
    def base_link(self):
        if self._base_link is None:
            self._base_link = "/".join([self.link, self.api_version, self.base_object])

        return self._base_link

    @property
    def productfolder(self):
        return f"{self.base_link}/productfolder"

    @property
    def assortment(self):
        return f"{self.base_link}/assortment"

    @property
    def product(self):
        return f"{self.base_link}/product"

    @property
    def counterparty(self):
        return f'{self.base_link}/counterparty'

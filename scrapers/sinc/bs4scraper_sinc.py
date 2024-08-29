import json
from typing import Iterable
from bs4 import BeautifulSoup, ResultSet
import requests
from fake_useragent import UserAgent


class ParserBS4:
    """
    Класс для парсинга сайта с помощью BeautifulSoup4.

    params: url: str: url сайта.
    params: session: requests.Session: объект для работы с сайтом.
    params: base_url: str: domain сайта.
    params: category_href: bool: Флаг необходимости получения ссылки на категорию.
    params: item_href: bool: Флаг необходимости обработки карточки товара.

    methods:
    get_html(self) -> str: метод для получуения html сайта.
    get_soup(self, url:str = None) -> BeautifulSoup: метод для получения обьекты bs4.soup html сайта.
    get_category(self): -> str: метод для получения категории сайта.
    get_page(self) -> int: метод для получения номера страницы сайта.
    get_items(self) -> ResultSet: метод для получения элементов сайта.
    inspect_item(self) -> Iterable: метод для получения информации об обьекте.
    save_item(self) -> None: метод для сохранения информации об обьекте.
    """

    def __init__(self, url: str, category_href: bool = True, item_href: bool = True):
        self.url: str = url
        self.session = requests.Session()
        self.base_url: str = 'https://parsinger.ru/html/'
        self.category_href: bool = category_href
        self.item_href: bool = item_href

    def get_html(self, url: str) -> str:
        """Метод для получения html сайта

        params: url: str: Url сайта.

        return: str: html сайта."""
        response = self.session.get(url=url,
                                    headers={'User-Agent': UserAgent().random},
                                    timeout=5)
        response.encoding = 'utf-8'
        return response.text

    def get_soup(self, url: str = None) -> BeautifulSoup:
        """Метод для получения обьекты bs4.soup html сайта

        :param url: str:  (Default value = None) Url сайта.

        :return: BeautifulSoup: обьект bs4.soup
        """
        if url is None:
            url = self.url
        return BeautifulSoup(self.get_html(url), 'lxml')

    def get_category(self) -> str:
        """Генератор для получения категории сайта"""
        soup = self.get_soup()
        for category in soup.select_one('div.nav_menu').select('a'):
            yield category.get('href')

    def get_page(self) -> str:
        """Пумератор для получения номера страницы сайта"""
        if self.category_href:
            for category in self.get_category():
                soup = self.get_soup(self.base_url + category)
                for page in soup.select_one('div.pagen').select('a'):
                    yield page.get('href')
        else:
            soup = self.get_soup()
            for page in soup.select_one('div.pagen').select('a'):
                yield page.get('href')

    def get_item(self) -> ResultSet:
        """Генератор для получения обьктов сайта"""
        for items in self.get_page():
            soup = self.get_soup(self.base_url + items)
            for item in soup.select('div.item'):
                yield item

    def inspect_item(self) -> Iterable:
        """Метод для получения информации об обьекте"""
        if self.item_href:
            for item_page in self.get_item():
                soup: BeautifulSoup = self.get_soup(self.base_url + item_page)
                for item in soup.select('div.item'):
                    name: str = item.select_one('a.name_item').text.strip()
                    description: list = [desc.text.split(':')[1].strip() for desc in item.select('li')]
                    price: str = item.select_one('div.price_box p.price').text.strip()
                    yield name, *description, price
        else:
            for item_block in self.get_page():
                soup: BeautifulSoup = self.get_soup(self.base_url + item_block)
                for item in soup.select('div.item'):
                    item_dict:  dict = {}
                    name: str = item.select_one('a.name_item').text.strip()
                    item_dict['Наименование'] = name
                    description: dict = {desc.text.split(':')[0].strip(): desc.text.split(':')[1].strip()
                                         for desc in item.select('li')}
                    item_dict.update(description)
                    price: str = item.select_one('div.price_box p.price').text.strip()
                    item_dict['Цена'] = price
                    yield item_dict

    def save_item(self) -> None:
        """Метод сохранения информации об обьекте"""
        result: list = []
        for item_dict in self.inspect_item():
            result.append(item_dict)
        with open('all_items.json',  'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

import time
import json
from typing import Iterable
from bs4 import BeautifulSoup, ResultSet
import requests
import re
import csv
from fake_useragent import UserAgent


class Parser:

    def __init__(self, url: str, category_href: bool = True, item_href: bool = True):
        self.url: str = url
        self.session = requests.Session()
        self.base_url: str = 'https://parsinger.ru/html/'
        self.category_href: bool = category_href
        self.item_href: bool = item_href


    def get_html(self, url) -> str:
        response = self.session.get(url=url,
                         headers={'User-Agent': UserAgent().random},
                        timeout=5)
        response.encoding = 'utf-8'
        return response.text

    def parse(self, url: str = None) -> BeautifulSoup:
        if url is None:
            url = self.url
        return BeautifulSoup(self.get_html(url), 'lxml')

    def get_category(self) -> str:
        soup = self.parse()
        for category in soup.select_one('div.nav_menu').select('a'):
            yield category.get('href')

    def get_page(self) -> str:
        if self.category_href:
            for category in self.get_category():
                soup = self.parse(self.base_url+category)
                for page in soup.select_one('div.pagen').select('a'):
                    yield page.get('href')
        else:
            soup = self.parse()
            for page in soup.select_one('div.pagen').select('a'):
                yield page.get('href')

    def get_item(self) -> ResultSet:
        for items in self.get_page():
            soup = self.parse(self.base_url+items)
            for item in soup.select('div.item'):
                yield item

    def inspect_item(self) -> Iterable:
        if self.item_href:
            for item_page in self.get_item():
                soup: BeautifulSoup = self.parse(self.base_url+item_page)
                for item in soup.select('div.item'):
                    name: str = item.select_one('a.name_item').text.strip()
                    description: list = [desc.text.split(':')[1].strip() for desc in item.select('li')]
                    price: str = item.select_one('div.price_box p.price').text.strip()
                    yield name, *description, price
        else:
            for item_block in self.get_page():
                soup: BeautifulSoup = self.parse(self.base_url+item_block)
                for item in soup.select('div.item'):
                    item_dict:  dict = {}
                    name: str = item.select_one('a.name_item').text.strip()
                    item_dict['Наименование'] = name
                    description: dict = {desc.text.split(':')[0].strip(): desc.text.split(':')[1].strip() for desc in item.select('li')}
                    item_dict.update(description)
                    price: str = item.select_one('div.price_box p.price').text.strip()
                    item_dict['Цена'] = price
                    yield item_dict

    def save_item(self) -> None:
        result: list = []
        for item_dict in self.inspect_item():
            result.append(item_dict)
        with open('all_items.json',  'w', encoding='utf-8') as file:
                json.dump(result, file, indent=4, ensure_ascii=False)


parser = Parser('https://parsinger.ru/html/index1_page_1.html'
                , item_href=False)

parser.save_item()





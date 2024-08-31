from typing import Optional

import aiohttp
import asyncio
from bs4 import BeautifulSoup, Tag, ResultSet
from fake_useragent import UserAgent


class AsyncParser:
    """Класс для асинхронного парсера

    params: base_url: str: - основной адрес сайта

    params: loop: asyncio.AbstractEventLoop:- объект для работы с event loop

    """

    def __init__(self, base_url: str, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.pages = None
        self.loop = loop
        self.base_url = base_url

    async def get_pages_href(self, url: str) -> list[str]:
        """Метод для переход на основной сайт и получение списка url страниц пагинации втекущей категории

        params: url: str: - адрес первой страницы для парсинга

        return: list[str]: - список url страниц пагинации втекущей категории
        """
        async with aiohttp.ClientSession(base_url=self.base_url,
                                         loop=self.loop,
                                         headers={'headers': UserAgent().random},
                                         trust_env=True) as session:
            async with session.get(f"/html/{url}") as response:
                soup: BeautifulSoup = BeautifulSoup(await response.text(), 'lxml')
                pages: ResultSet[Tag] = soup.select_one('div.pagen').select('a')
                return [page['href'] for page in pages]

    async def get_items_cards(self, url: str):
        """Получение карточек обьктов со страницы

        params: url: str: - адрес страницы для парсинга и получения карточек обьктов

        return: list[dict]: - список карточек обьктов со страницы"""

        async with aiohttp.ClientSession(base_url=self.base_url,
                                         loop=self.loop,
                                         headers={'headers': UserAgent().random},
                                         trust_env=True) as session:
            async with session.get(f"/html/{url}") as response:
                soup: BeautifulSoup = BeautifulSoup(await response.text(), 'lxml')
                cards: ResultSet[Tag] = soup.select('a.name_item')
                return [card['href'] for card in cards]

    async def get_information_about_item_from_card(self, url: str):
        """Получение информации обьекта со страницы

        params: url: str: - адрес страницы для парсинга и получения информации об обьекте

        """
        async with aiohttp.ClientSession(base_url=self.base_url,
                                         loop=self.loop,
                                         headers={'headers': UserAgent().random},
                                         trust_env=True) as session:
            async with session.get(f"/html/{url}") as response:
                soup: BeautifulSoup = BeautifulSoup(await response.text(), 'lxml')
                description: Tag = soup.select_one('div.description')
                header: Tag = description.select_one('p#p_header').text.strip()
                article: Tag = description.select_one('p.article').text.strip()
                descriptions = [description.text.strip() for description in description.select('ul#description>li')]
                in_stock = description.select_one('span#in_stock').text.strip()
                price = description.select_one('span#price').text.strip()
                old_price = description.select_one('span#old_price').text.strip()
                return header, article, *descriptions, in_stock, price, old_price




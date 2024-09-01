import json
import os

import asyncio
import pytest

from scrapers.async_parsers.async_parser import AsyncParser


class TestAsyncParser:
    parser = AsyncParser(base_url='https://parsinger.ru')

    @pytest.mark.asyncio
    async def test_async_get_get_pages_href(self):
        parser = AsyncParser(base_url='https://parsinger.ru', loop=asyncio.get_event_loop())
        pages: list = await parser.get_pages_href(url='index2_page_1.html')

        assert len(pages) == 4
        assert pages[0] == 'index2_page_1.html'
        assert pages[-1] == 'index2_page_4.html'

    @pytest.mark.asyncio
    async def test_get_items_cards(self):
        parser = AsyncParser(base_url='https://parsinger.ru', loop=asyncio.get_event_loop())
        cards: list = await parser.get_items_cards(url='index2_page_1.html')

        assert len(cards) == 8
        assert cards[0] == 'mobile/2/2_1.html'
        assert cards[-1] == 'mobile/2/2_8.html'

    @pytest.mark.asyncio
    async def test_get_information_about_item_from_card(self):
        parser = AsyncParser(base_url='https://parsinger.ru', loop=asyncio.get_event_loop())
        card_info: list = await parser.get_information_about_item_from_card(url='mobile/2/2_1.html')

        assert card_info['name'] == 'teXet TM-519R черный-красный Мобильный телефон'
        assert card_info['article'] == '80397881'
        assert card_info['description']['model'] == 'TM-519R'

        assert card_info['count'] == '31'
        assert card_info['price'] == '2490 руб'
        assert card_info['old_price'] == '2520 руб'

    @pytest.mark.asyncio
    async def test_save_information_about_items(self):
        parser = AsyncParser(base_url='https://parsinger.ru', loop=asyncio.get_event_loop())
        data = [{"categories": "mobile", 'name': 'test_item', 'article': '12345'},
                {'categories': 'mobile', 'name': 'test_item', 'article': '67890'}]
        parser.save_information_about_items(data)

        with open('data.json', 'r') as f:
            assert json.load(f) == data
            os.remove('data.json')

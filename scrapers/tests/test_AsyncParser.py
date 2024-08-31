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
        description, asrticle, brand, moddel, *_, in_stock, price, old_price = card_info
        assert description == 'teXet TM-519R черный-красный Мобильный телефон'
        assert asrticle == 'Артикул: 80397881'
        assert brand == 'Бренд: Texet'
        assert moddel == 'Модель: TM-519R'

        assert in_stock == 'В наличии: 31'
        assert price == '2490 руб'
        assert old_price == '2520 руб'



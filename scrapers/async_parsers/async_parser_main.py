import asyncio

from async_parser import AsyncParser


async def main():
    parser = AsyncParser(base_url='https://parsinger.ru')
    pages = await parser.get_pages_href(url='index2_page_1.html')
    cards_list = await asyncio.gather(*[parser.get_items_cards(url=page) for page in pages])
    items_list = await asyncio.gather(*[parser.get_information_about_item_from_card(card)
                                        for chunk_cards in cards_list for card in chunk_cards])
    parser.save_information_about_items(items_list)


if __name__ == '__main__':
    asyncio.run(main())

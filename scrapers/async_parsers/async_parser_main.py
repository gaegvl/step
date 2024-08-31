import asyncio

from async_parser import AsyncParser


async def main():
    parser = AsyncParser(base_url='https://parsinger.ru')
    pages = await parser.get_pages_href(url='index2_page_1.html')
    page = pages[0]
    cards = await parser.get_items_cards(page)

if __name__ == '__main__':
    asyncio.run(main())


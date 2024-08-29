from bs4scraper_sinc import ParserBS4


parser = ParserBS4('https://parsinger.ru/html/index1_page_1.html'
                   , item_href=False)

parser.save_item()

# Ресурс:
# Avito.ru
# Раздел Недвижимость Квартиры
#
# Необходимо обойти все предложения в разделе Недвижимость Квартиры и собрать следующие данные:
#
# Название, Ссылки на все фото, Стоимость, URL объявления, URL автора объявления, Адрес местоположения объекта
#
# Данные сохраняем в SQLlite базу данных. (Связи делать не надо, их сложно контролировать, но если кто-то хочет может реализовать связь объявления и автора)
#
# ВНИМАНИЕ: Авито очень агрессивен на парсеров, снизте количество одновременных запросов на домен до минимума. Более 5 вообще ставить не рекомендую.

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from hh_scraping import settings
from hh_scraping.spiders.hh_vacancy import HhVacancySpider
from hh_scraping.spiders.avito import AvitoSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings = crawler_settings)
    process.crawl(AvitoSpider)
    process.start()
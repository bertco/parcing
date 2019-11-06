# Источник Avito Авто
#
# Выбираем раздел автомобилей . Обходим всю пагинацию, скачиваем и сохраняем фото.
#
# В структуре записи должны присутсвовать следующие данные:
#
# Заголовок
# Цена
#
# характеристики (https://www.dropbox.com/s/x72sfec0j48td7n/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%202019-10-25%2022.24.37.png?dl=0)
#
# Подробные характеристики сокрытые за кнопкой (https://www.dropbox.com/s/7ojygvq8hdnw9ug/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%202019-10-25%2022.25.28.png?dl=0)
#
# Фото
# Данные по VIN из официальных баз данных
#
# собираем максимальное колличество данных, стараемся обработать таким образом, что-бы в последсвии поиск по базе был максимально удобным

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from hh_scraping import settings
from hh_scraping.spiders.hh_vacancy import HhVacancySpider
from hh_scraping.spiders.avito import AvitoSpider
from hh_scraping.spiders.avito_car import AvitoCarSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings = crawler_settings)
    process.crawl(AvitoCarSpider)
    process.start()
# Источник данных:
# https://hh.ru
#
# Ваша задача по любому ключевому слову получить список вакансий.
#
# сохранить в монго:
#
# заголовок вакансии
# название и ссылку(страница hh) на компанию разместившую вакансию
# Ссылку на оф сайт компании разместившую вакансию.
# Все ключевые навыки
# предлагаемую ЗП
#
# Задание реализовывать используя Scrapy

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from hh_scraping import settings
from hh_scraping.spiders.hh_vacancy import HhVacancySpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings = crawler_settings)
    process.crawl(HhVacancySpider)
    process.start()


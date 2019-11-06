# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from hh_scraping.items import AvitoCar

class AvitoCarSpider(scrapy.Spider):
    name = 'avito_car'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/kazan/avtomobili']

    def parse(self, response:HtmlResponse):

        next_page = response.xpath(
            '//div[contains(@class, "pagination")]/'
            'div[contains(@class, "pagination-nav")]/'
            'a[contains(@class, "js-pagination-next")]/@href'
        ).extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        car_pages = response.xpath(
            '//a[contains(@class, "item-description-title-link")]/@href'
        ).extract()

        if car_pages is None:
            print('error car_pages')

        for car in car_pages:
            yield response.follow(car, callback=self.parse_page)

    def parse_page(self, response: HtmlResponse):

        id_post = response.url.split('_')[-1]

        add_spec_url = f'https://www.avito.ru/js/items/{id_post}/car_spec?'
        add_spec_urt_data = requests.get(add_spec_url)
        add_spec = add_spec_urt_data.json().get('spec').get('blocks')

        vin_data_url = f'https://www.avito.ru/web/1/swaha/v1/autoteka/teaser/{id_post}?unlockCrashes=false'
        vin_data_urt_data = requests.get(vin_data_url)
        vin_data = vin_data_urt_data.json().get('result').get('insights')

        item = ItemLoader(AvitoCar(), response)
        item.add_xpath('title', '//h1[@class="title-info-title"]/span[@class="title-info-title-text"]/text()')
        item.add_xpath('price', '//span[@itemprop="price"]/text()')
        item.add_xpath('images', '//div[contains(@class, "js-gallery-img-frame")]/@data-url')
        item.add_xpath('options', '//div[@class="item-params"]/ul[@class="item-params-list"]/li')

        item.add_value('additional_options', add_spec)
        item.add_value('vin_data', vin_data)

        yield item.load_item()



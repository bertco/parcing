# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/kazan/kvartiry/prodam?cd=1']

    def parse(self, response: HtmlResponse):
        pagination = response.xpath(
            '//a[contains(@class, "pagination-page")]/@href'
        ).extract_first()

        if pagination is not None:
            yield response.follow(pagination, callback=self.parse)

        apt_pages = response.xpath(
            '//a[contains(@class, "item-description-title-link")]/@href'
        ).extract()

        if apt_pages is None:
            print('error apt_pages')

        # for apt in apt_pages:
        #     item = {
        #         'post url': apt
        #     }
        #     yield response.follow(apt, callback=self.parse_apt_page, cb_kwargs={'item': item})

        for apt in apt_pages:
            yield response.follow(apt, callback=self.parse_page)

    def parse_page(self, response: HtmlResponse):

        title = response.xpath(
            '//h1[@class="title-info-title"]/span[@class="title-info-title-text"]/text()'
        ).extract_first()

        if title is None:
            print('error title')

        # image_urls = response.xpath(
        #     '//div[contains(@class, "js-gallery-img-frame")]/@data-url'
        # ).extract()

        price = response.xpath(
            '//span[@itemprop="price"]/text()'
        ).extract_first()

        if price is None:
            print('error price')

        post_url = response.url

        if post_url is None:
            print('error post_url')

        author_url = response.xpath(
            '//div[contains(@class, "js-seller-info-name")]/a/@href'
        ).extract_first()

        if author_url is None:
            print('error author_url')

        address = response.xpath(
            '//div[@class="item-address"]/span[@class="item-address__string"]/text()'
        ).extract_first()

        if address is None:
            print('error address')

        item = {
            'title': title,
            # 'image_urls': image_urls,
            'price': price,
            'post_url': post_url,
            'author_url': author_url,
            'address': address
        }

        yield item

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_images(item):
    if item[:2] == '//':
        return f'http:{item}'
    return item

def cleaner_options(item):

    result = item.split('">')[-1].split(':')
    key = result[0]
    value = result[-1].split(" </li>")[0].split(' </span>')[-1]
    return {key: value}

def dict_options(items):
    result = {}
    for item in items:
        result.update(item)

    return result

def dict_vin_data(items):
    result = {}
    for i in items:
        result[i['text']] = i['status']

    return result

def dict_add_options(items):
    result = {}
    for item in items:
        result_1 = []

        for i in item['params']:
            result_2 ={}
            if i['name'][-1] == '.':
                i['name'] = f"{i['name'].split('.')[0]} {i['name'].split('.')[1]}"
            result_2[i['name']] = i['value']
            result_1.append(result_2)

        result[item['title']] = result_1

    return result

class HhScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AvitoCar(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    options = scrapy.Field(input_processor=MapCompose(cleaner_options), output_processor=dict_options)
    images = scrapy.Field(input_processor=MapCompose(cleaner_images))
    additional_options = scrapy.Field(output_processor=dict_add_options)
    vin_data = scrapy.Field(output_processor=dict_vin_data)


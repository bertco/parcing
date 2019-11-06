# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from sqldatabase.database import BlogBase
from sqldatabase.models_avito import AptPost, Authors, Base
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class HhScrapingPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        self.avito_db = client.avito


        # bd_url = r'sqlite:///C:\Users\\alber\\PycharmProjects\\GB_Basics\\avito_17.sqlite'
        # self.bd = BlogBase(Base, bd_url)

    def process_item(self, item, spider):

        # author = Authors(item.get('author_url'))
        # try:
        #     self.bd.session.add(author)
        #     self.bd.session.commit()
        # except Exception:
        #
        #     author = self.bd.session.query(Authors).filter_by(url=item.get('author_url')).first()

        # aptpost = AptPost(
        #     item['title'], item['post_url'], item['price'], item['author_url'], item['address']
        # )
        #
        # self.bd.session.add(aptpost)
        # self.bd.session.commit()

        # self.hh_collection.insert_one(item)

        collection = self.avito_db[spider.name]
        collection.insert_one(item)
        return item

class AvitoImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['images']:
            for image in item['images']:
                try:
                    yield scrapy.Request(image)
                except Exception as e:
                    pass

    def item_completed(self, results, item, info):
        if results:
            item['images'] = [item[1] for item in results if item[0]]
        return item
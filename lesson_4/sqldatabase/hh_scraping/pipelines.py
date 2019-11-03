# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from sqldatabase.database import BlogBase
from sqldatabase.models_avito import AptPost, Authors, Base

class HhScrapingPipeline(object):
    def __init__(self):
        # mongo_url = 'mongodb://localhost:27017'
        # client = MongoClient(mongo_url)
        # hh_db = client.hh
        # self.hh_collection = hh_db.hh_vacancy_DS
        bd_url = r'sqlite:///C:\Users\\alber\\PycharmProjects\\GB_Basics\\avito_14.sqlite'
        self.bd = BlogBase(Base, bd_url)

    def process_item(self, item, spider):


        # author = Authors(item.get('author_url'))
        # try:
        #     self.bd.session.add(author)
        #     self.bd.session.commit()
        # except Exception:
        #
        #     author = self.bd.session.query(Authors).filter_by(url=item.get('author_url')).first()

        aptpost = AptPost(
            item['title'], item['post_url'], item['price'], item['author_url'], item['address']
        )

        self.bd.session.add(aptpost)
        self.bd.session.commit()


        # self.hh_collection.insert_one(item)
        return item
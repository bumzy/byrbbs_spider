# -*- coding: utf-8 -*-
import pymongo
import functools
from scrapy.conf import settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

def check_pipline(func):
    @functools.wraps(func)
    def wrapper(self, item, spider):
        if self.__class__.__name__ in spider.pipeline:
            return func(self, item, spider)
        else:
            return item
    return wrapper

class ByrSectionPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL_SECTION']]  # 获得collection的句柄
    @check_pipline
    def process_item(self, item, spider):
        self.coll.insert(dict(item))
        return item

class ByrArticlePipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL_ARTICLE']]  # 获得collection的句柄
    @check_pipline
    def process_item(self, item, spider):
        self.coll.insert(dict(item))
        return item


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from daomu import settings
import pymysql
import pymongo

class DaomuPipeline(object):
    def process_item(self, item, spider):
        print("++++++++++++++++++++++")
        print(item["bookName"])
        print(item["bookTitle"])
        print(item["zhName"])
        print(item["zhNum"])
        print(item["zhLink"])
        print("==================")

class DaomumongoPipeline(object):
    def __init__(self):
        # 从settings.py中获取变量的值
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        # 创建数据库连接对象、库对象、集合对象
        conn = pymongo.MongoClient(host=host,port=port)
        db = conn.daomudb
        self.myset = db.daomubiji

    def process_item(self,item,spider):
        bookInfo = dict(item)
        self.myset.insert(bookInfo)
        print("OK")


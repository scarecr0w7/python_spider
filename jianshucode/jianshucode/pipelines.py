# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from twisted.enterprise import adbapi
from pymysql import cursors


class JianshucodePipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.dbparams = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'port': 3306,
            'database': 'jianshu',
            'charset': 'utf8'
        }

    def open_spider(self, spider):
        self.db = pymysql.connect(**self.dbparams)
        self.cursor = self.db.cursor()
        self.sql = 'insert into jianshu_all_writings(title, author, content, pub_time, like_num, read_num) values(%s, %s, %s, %s, %s, %s)'

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (
            item['title'], item['author'], item['content'], item['pub_time'], item['like_num'], item['read_num']))
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()


# 异步
class MysqlTwistedPipeline(object):
    def __init__(self):
        self.dbparams = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'port': 3306,
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **self.dbparams)
        self.sql = 'insert into jianshu_all_writings(title, author, content, pub_time, like_num, read_num) values(%s, %s, %s, %s, %s, %s)'

    def process_item(self, item, spider):
        result = self.dbpool.runInteraction(self.insert_data, item)
        result.addCallback(self.handle_error, item, spider)

    def insert_data(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['author'], item['content'], item['pub_time'], item['like_num'], item['read_num']))

    def handle_error(self, error, item, spider):
        print('*'*30)
        print(error)

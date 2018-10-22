# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from twisted.enterprise import adbapi
from scrapy.mail import MailSender
import pymysql
import pymysql.cursors


class LexisPipeline(object):
    def __init__(self, dbpool, settings):
        self.dbpool = dbpool
        self.settings = settings
    @classmethod
    def from_settings(cls, settings):
        dbpool = adbapi.ConnectionPool("pymysql", host=settings["MYSQL_HOST"], db=settings["MYSQL_DBNAME"],
                                       user=settings["MYSQL_USER"], password=settings["MYSQL_PASSWORD"], charset="utf8mb4",
                                       cursorclass=pymysql.cursors.DictCursor,
                                       use_unicode=True)
        return cls(dbpool, settings)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        self.dbpool.runInteraction(self.do_insert, item)

    def close_spider(self, spider):

        # mailer = MailSender()
        mailer = MailSender.from_settings(self.settings)
        mailer.send(to=["1174955828@qq.com"], subject="Some subject", body="Some body", cc=[])

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

class EmptyPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):

        return item
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LexisItem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into lexis(id, title, href) values (null, %s, %s)"
        params = (
            self['title'], self['href']
        )
        return insert_sql, params

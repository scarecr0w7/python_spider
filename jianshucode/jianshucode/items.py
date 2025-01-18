# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshucodeItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    pub_time = scrapy.Field()
    like_num = scrapy.Field()
    read_num = scrapy.Field()

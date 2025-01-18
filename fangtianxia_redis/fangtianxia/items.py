# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    sheng = scrapy.Field()
    shi = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    house_type = scrapy.Field()
    area = scrapy.Field()
    is_sale = scrapy.Field()
    tags = scrapy.Field()
    new_link = scrapy.Field()


class EsfItem(scrapy.Item):
    sheng = scrapy.Field()
    shi = scrapy.Field()
    title = scrapy.Field()
    house_type = scrapy.Field()
    area = scrapy.Field()
    year = scrapy.Field()
    floor = scrapy.Field()
    direction = scrapy.Field()
    people = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    unit_price = scrapy.Field()
    esf_link = scrapy.Field()

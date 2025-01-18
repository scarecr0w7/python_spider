# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshucode.items import JianshucodeItem

class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/p/.+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = JianshucodeItem()

        item['title'] = response.xpath('//h1[contains(@class,"_1RuRku")]/text()').get()
        print(item['title'])
        num = response.xpath('//div[contains(@class,"s-dsoj")]/span/text()').getall()
        item['read_num'] = num[1].split()[1]
        item['like_num'] = response.xpath('//span[@class="_3tCVn5"]/span/text()').get()
        item['pub_time'] = response.xpath('//div[contains(@class,"s-dsoj")]/time/text()').get()
        item['author'] = response.xpath('//span[@class="_22gUMi"]/text()').get()
        contents = response.xpath('//article[contains(@class,"_2rhmJa")]/p/text()').getall()
        item['content'] = ''.join(contents)

        return item

# -*- coding: utf-8 -*-
import scrapy
import re
from fangtianxia.items import NewHouseItem, EsfItem
from scrapy_redis.spiders import RedisSpider


class FangSpider(RedisSpider):
    name = 'fang'
    allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']
    # 设置起始的url，在redis中写入fang:start_urls，值应为初始url
    redis_key = 'fang:start_urls'

    def parse(self, response):
        trs = response.xpath('//tr')
        sheng = None
        for tr in trs:
            sheng_text = tr.xpath('./td[2]//text()').get()
            sheng_text = re.sub(r'\s', '', sheng_text)
            if sheng_text:
                sheng = sheng_text
            if sheng == '其它':
                continue
            shi_list = tr.xpath('./td[3]/a')
            for s in shi_list:

                shi = s.xpath('./text()').get()
                link = s.xpath('./@href').get()

                if shi == '北京':
                    esf_url = 'https://esf.fang.com/'
                    new_house_url = 'https://newhouse.fang.com/house/s/'
                elif sheng == '台湾':
                    # new_house_url = 'http://www.twproperty.com.tw/'
                    # esf_url = None
                    continue
                elif sheng == '香港':
                    # esf_url = 'https://hk.esf.fang.com/'
                    # new_house_url = None
                    continue
                else:
                    # 基础url http://mianyang.fang.com/
                    # 二手房url https://mianyang.esf.fang.com/
                    links = link.split('fang')
                    http = links[0]
                    # https = re.sub(r'http', 'https', http)
                    com = links[1]
                    esf_url = http + 'esf.fang' + com
                    # 新房url https://mianyang.newhouse.fang.com/house/s/
                    new_house_url = http + 'newhouse.fang' + com + 'house/s/'

                yield scrapy.Request(new_house_url, callback=self.new_house_parse, meta={'info': (sheng, shi)})

                yield scrapy.Request(esf_url, callback=self.esf_parse, meta={'info': (sheng, shi)})

    def new_house_parse(self, response):
        sheng, shi = response.meta['info']
        item = NewHouseItem()
        item['sheng'] = sheng
        item['shi'] = shi
        lis = response.xpath('//div[contains(@class, "nl_con")]/ul/li')
        for li in lis:
            name = li.xpath('.//div[@class="nlcd_name"]/a/text()').get()
            item['name'] = re.sub(r'\s', '', str(name))

            new_link = li.xpath('.//div[@class="nlcd_name"]/a/@href').get()
            item['new_link'] = response.urljoin(new_link)

            item['address'] = li.xpath('.//div[@class="address"]/a/@title').get()

            house_type_li = li.xpath('.//div[contains(@class, "house_type")]/a/text()').getall()
            # 匹配有居的项，有则加入列表
            house_type = [house for house in house_type_li if re.search('居', house)]
            item['house_type'] = '/'.join(house_type)

            area = li.xpath('.//div[contains(@class, "house_type")]/text()').getall()
            area = list(map(lambda x: re.sub(r'\s|/|－', '', str(x)), area))
            item['area'] = ''.join(area)

            item['is_sale'] = li.xpath('.//div[contains(@class,"fangyuan")]/span/text()').get()

            tags = li.xpath('.//div[contains(@class,"fangyuan")]/a/text()').getall()
            item['tags'] = '/'.join(tags)

            prices = li.xpath('.//div[@class="nhouse_price"]//text()').getall()
            price = list(map(lambda p: re.sub(r'\s|广告', '', str(p)), prices))
            item['price'] = ''.join(price)

            yield item

        next_url = response.xpath('.//a[@class="next"]/@href').get()
        next = response.xpath('.//a[@class="next"]/text()').get()
        if next == '下一页':
            yield scrapy.Request(response.urljoin(next_url), callback=self.new_house_parse, meta={'info': (sheng, shi)})

    def esf_parse(self, response):
        sheng, shi = response.meta['info']
        item = EsfItem()
        item['sheng'] = sheng
        item['shi'] = shi
        dls = response.xpath('//div[contains(@class,"shop_list")]/dl')

        print(sheng, shi)
        for dl in dls:
            item['title'] = dl.xpath('.//span[@class="tit_shop"]/text()').get()

            esf_link = dl.xpath('.//h4[@class="clearfix"]/a/@href').get()
            item['esf_link'] = response.urljoin(esf_link)

            tel_shop = dl.xpath('./dd[1]/p[1]//text()').getall()
            tel_shop = list(map(lambda d: re.sub(r'\s|\|', '', d), tel_shop))
            for shop in tel_shop:
                if '厅' in shop:
                    item['house_type'] = shop
                elif '㎡' in shop:
                    item['area'] = shop
                elif '层' in shop:
                    item['floor'] = shop
                elif '向' in shop:
                    item['direction'] = shop
                elif '年建' in shop:
                    item['year'] = shop

            item['name'] = dl.xpath('./dd[1]/p[2]/a/@title').get()

            item['address'] = dl.xpath('./dd[1]/p[2]/span/text()').get()

            item['people'] = dl.xpath('./dd[1]/p[1]/span/a/text()').get()

            price = dl.xpath('./dd[2]/span[1]//text()').getall()
            item['price'] = ''.join(price)

            item['unit_price'] = dl.xpath('./dd[2]/span[2]/text()').get()

            yield item

        next_url = response.xpath('//div[@class="page_al"]/p[1]/@href').get()
        next = response.xpath('//div[@class="page_al"]/p[1]/text()').get()

        if next == '下一页':
            yield scrapy.Request(next_url, callback=self.esf_parse, meta={'info': (sheng, shi)}, dont_filter=True)

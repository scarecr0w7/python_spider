import requests
import queue
import pymysql
from lxml import etree
import threading
import re


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    }


class MyThread(threading.Thread):
    def __init__(self, url_queue, lock):
        super(MyThread, self).__init__()
        self.url_queue = url_queue
        self.lock = lock

        self.cnn = pymysql.connect(host='localhost', user='root', password='', port=3306, database='news', charset='utf8')
        self.cursor = self.cnn.cursor()
        self.sql = 'insert into guanchazhe(title, author, publish_time, content, url) values(%s, %s, %s, %s, %s)'

    def run(self):
        self.spider()

    def spider(self):
        while not self.url_queue.empty():
            item = {}
            url = self.url_queue.get()
            print(f'正在爬取{url}')
            response = requests.get(url, headers=headers)
            response.encoding = "utf-8"
            html = etree.HTML(response.text)
            results = html.xpath('//ul/li[contains(@class,"left left-main")]')

            for result in results:
                item['title'] = result.xpath('./h3/text()')[0]

                author = result.xpath('./ul/li/div[contains(@class,author-intro)]/p/a/text()')
                if not author:
                    author = html.xpath('//div[contains(@class,"time")]/span[3]/text()')
                    if not author:
                        # author = html.xpath('//div[contains(@class,"user-photo")]//following-sibling::*[1]/div[@class="user-nick"]/a/text()')
                        author = ['unknown', ]
                item['author'] = author[0]

                item['publish_time'] = result.xpath('./div[contains(@class,"time")]/span[1]/text()')[0]

                content = result.xpath('./div[contains(@class,"content")]/p/text()')
                content = ''.join(content)
                content = re.sub('\s', '', content)
                item['content'] = content

                item['url'] = url

                self.lock.acquire()
                self.save(item)
                self.lock.release()

    def save(self, item):
        self.cursor.execute(self.sql, [item['title'], item['author'], item['publish_time'], item['content'], item['url']])
        self.cnn.commit()


def add_urls(urls, queue):
    for url in urls:
        url = 'https://www.guancha.cn' + url
        queue.put(url)


def get_url(queue):
    url = 'https://www.guancha.cn/'
    response = requests.get(url, headers=headers).text
    html = etree.HTML(response)
    left_urls = html.xpath('//ul[contains(@class, "Review-item")]/li/a[contains(@class, "module-img")]/@href')
    center_right_urls = html.xpath('//ul[contains(@class, "img-List")]/li/h4[contains(@class, "module-title")]/a/@href')
    add_urls(left_urls, queue)
    add_urls(center_right_urls, queue)


if __name__ == '__main__':
    threads = []
    lock = threading.Lock()

    url_que = queue.Queue()
    get_url(url_que)

    for i in range(10):
        thread = MyThread(url_que, lock)
        threads.append(thread)
        thread.start()
import scrapy
import re
from scrapy import Request
from douban_image_frank.items import DoubanImageFrankItem

class download_douban_image(scrapy.Spider):
    name = "douban_imgs"

    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def __init__(self, url='1638835355', *args, **kwargs):
        self.allowed_domains = "douban.com"
        self.start_urls = [
            'http://www.douban.com/photos/album/%s/' % (url)
        ]
        self.url = url

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url = url, headers=self.default_headers, callback=self.parse)


    def parse(self, response):
        list_imgs = response.xpath('//div[@class="photolst clearfix"]//img/@src').extract()
        if list_imgs:
            item = DoubanImageFrankItem()
            item['image_urls'] = list_imgs
            yield item

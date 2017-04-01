import scrapy
from douban_frank.items import BookItem

class BookSpider(scrapy.Spider):
    name = "douban_book"
    start_urls = [
        'https://book.douban.com/top250'
    ]
    allowed_domains = ["douban.com"]

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parse_book)
        print(response.url)
        for next_url in response.xpath('//div[@class="paginator"/a/@href').extrtor():
            if next_url:
                print(next_url)
                yield scrapy.Request(next_url, callback=self.parse_book)


    def parse_book(self, response):
        #//*[@id="content"]/div/div[1]/div/table[1]/tbody/tr/td[2]/div[1]/a
        #//*[@id="content"]/div/div[1]/div/table[4]/tbody/tr/td[2]/div[1]/a
        #//*[@id="content"]/div/div[1]/div[@class=

        #//*[@id="content"]/div/div[1]/div/table[1]/tbody/tr/td[2]/div[1]/a
        for table in response.xpath('//div[@class="indent"]'):
            name = table.xpath('table/tbody/tr/td/div[@class="pl2"]/a/text()').extract_first()
            info = table.xpath('table/tbody/tr/td/p[@class="pl"]/text()').extract_first()
            item = BookItem()
            item['name'] = name
            item['info'] = info
            yield item


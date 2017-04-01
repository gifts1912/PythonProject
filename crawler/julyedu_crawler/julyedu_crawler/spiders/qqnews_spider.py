import scrapy

class FinanceYahooSpider(scrapy.Spider):
    name = 'financeyahoo'
    start_urls = ['https://finance.yahoo.com/']

    def parse(self, response):
        #url xpath: //*[@id="slingstoneStream-0-Stream"]/ul/li/div/div/div[2]/h3/a
        for href in response.xpath('//*[@id="slingstoneStream-0-Stream"]/ul/li/div/div/div[2]/h3/a/@href'):
            fullUrl = response.urljoin(href.extract())
            print(fullUrl)
            yield scrapy.Request(fullUrl, callback = self.parse_passage)


    def parse_passage(self, response):
        #//*[@id="SideTop-0-HeadComponentTitle"]/h1
        title = response.xpath('//header/h1/text()').extract()[0]
        passage = '\n'.join(response.xpath('//article/div/p/text()').extract())
        print('title', title)
        print('passage', passage)
        print()
        yield {'title':title,
               'passage':passage
               }
from scrapy import cmdline

cmd_str = "scrapy crawl douban_book"

cmdline.execute(cmd_str.split(' '))
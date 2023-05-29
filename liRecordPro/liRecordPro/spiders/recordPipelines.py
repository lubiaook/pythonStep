import scrapy


class RecordpipelinesSpider(scrapy.Spider):
    name = "recordPipelines"
    start_urls = ["https://www.baidu.com"]

    def parse(self, response):
        pass

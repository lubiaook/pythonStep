import scrapy


class RecordSpider(scrapy.Spider):
    name = "record"
    # allowed_domains = ["www.pearvideo.com"]
    start_urls = ["https://www.pearvideo.com/popular"]

    def parse(self, response):
        # 抓取标题和概览
        # 直接在response后直接使用xpath获取解析
        ul_list = response.xpath('//*[@id="popularList"]/li')
        for li in ul_list:
            title = li.xpath('.//h2/text()').extract()
            print('标题为：', ''.join(title))
            # print('内容为：', li.xpath('.//p/text()'))
            # 列表元素为Select对象,使用extract()函数获取
            print('内容为：', li.xpath('.//p/text()')[0].extract())

        pass

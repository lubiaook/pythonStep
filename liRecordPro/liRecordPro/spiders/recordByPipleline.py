import scrapy

class ItemforPiple(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    pass

class RecordPipeline(scrapy.Spider):
    name = "recordPipeline"
    # allowed_domains = ["www.pearvideo.com"]
    start_urls = ["https://www.pearvideo.com/popular"]

    def parse(self, response):
        # 抓取标题和概览
        # 直接在response后直接使用xpath获取解析
        ul_list = response.xpath('//*[@id="popularList"]/li')
        for li in ul_list:
            title = li.xpath('.//h2/text()').extract()
            # print('标题为：', ''.join(title))
            title2 = ''.join(title)
            # print('内容为：', li.xpath('.//p/text()'))
            # 列表元素为Select对象,使用extract()函数获取
            # print('内容为：', li.xpath('.//p/text()')[0].extract())
            content = li.xpath('.//p/text()')[0].extract()
            # from liRecordPro.liRecordPro.items import LirecordproItem
            item = ItemforPiple()
            item['title'] = title2
            item['content'] = content
            # 发送给管道
            yield item
            # pipline = LirecordproPipeline
            # pipline.process_item(item)
        pass

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LirecordproPipeline:
    fp = None

    # def __init__(self):
    #     self.fb = None

    def open_spider(self, spider):
        print("开始爬虫")
        self.fp = open('./qiushi.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        print('标题：' + item['title'])
        print('内容：' + item['content'])
        self.fp.write('标题：' + item['title'] + ' 内容：' + item['content'] + ' \n')
        # self.fp.write('标题：' + item['title'])
        return item

    def end_spider(self, spider):
        print("结束爬虫")
        self.fp.close()

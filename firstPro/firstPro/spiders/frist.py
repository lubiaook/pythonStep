import scrapy


class FristSpider(scrapy.Spider):
    # 爬虫文件的名称，就是爬虫源文件的唯一标识
    name = "frist"
    # 允许的域名,用来限定 哪些start_url能被执行,通常不被使用，需要注释掉
    # allowed_domains = ["www.baidu.com"]
    # 起始的url列表:该列表中存放的url会被scrapy 自动进行请求发送
    start_urls = ["https://www.baidu.com","https://yiyan.baidu.com/","https://www.yimei180.com"]


    # 用于数据解析,response参数表示 请求成功后对应的响应对象。
    def parse(self, response):
        print(response)
        print('换行啦~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        pass

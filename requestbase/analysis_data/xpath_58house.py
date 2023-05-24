import requests
from lxml import etree

if __name__ == '__main__':
    url = 'https://bj.58.com/ershoufang/?PGTID=0d100000-0000-1961-a3da-2d92c0ae1216&ClickID=4'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=header)
    with open('./58.html', 'w', encoding='utf-8') as fp:
        fp.write(response.text)

        # print(response.text)
        etree = etree.HTML(response.text)
        # ex = etree.xpath('//div[@name="property-content-title"]')
        # print(ex)
        # h3ex = etree.xpath('//h3/@title')
        # for hs in h3ex:
        #     print(hs)

        # 将价格、和主标题存储
    list_content = etree.xpath('//div[@class="property-content"]')
    # print(list_content)
    for detail in list_content:
        title = detail.xpath('.//h3/@title')
        price =detail.xpath('.//span[@class="property-price-total-num"]/text()')
        print(title[0])
        print(price[0])

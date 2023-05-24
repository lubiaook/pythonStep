import requests
from lxml import etree

if __name__ == '__main__':
    # 本地 html加载到etree对象
    localETree = etree.parse('./local.html')
    # 获取title
    title = localETree.xpath('/html/head/title')
    div = localETree.xpath('/html/body/div')
    # 属性定位
    divClass = localETree.xpath('//div[@class="song"]')
    # 索引定位
    indexLocationClass=localETree.xpath('//div[@class="tang"]//li[5]/a/text()')[0]
    print(indexLocationClass)
    # 索引定位
    print(localETree.xpath("//li[7]//text()")[0])
    # 取属性
    print(localETree.xpath('//div[@class="song"]//img/@src')[0])
    print(localETree.xpath('//div[@class="song"]//img/@title')[0])


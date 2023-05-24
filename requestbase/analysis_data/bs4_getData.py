import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 本地的html加载到bfsoup对象中
    fp = open('./localdata.html', encoding='utf-8')
    localBeatifulSoup = BeautifulSoup(fp, 'lxml')
    print(localBeatifulSoup)
    # *.tagName 输出 返回文档中输出第一次出现的标签名
    print(localBeatifulSoup.a)
    print(localBeatifulSoup.div)
    # *.find('div)
    localBeatifulSoup.find('div')
    # soup.find('div') 查找 class 为song 的div
    localBeatifulSoup.find('div', class_='song')
    # soup.findAll('div') 的div 返回的是一个数组
    localBeatifulSoup.findAll('tagName')
    # soup.select('某种选择器，ID，class，标签选择器')
    localBeatifulSoup.select('.tang')
    # > 标识一个层级
    # 空格 标识多个层级
    localBeatifulSoup.select('.tang > ul > li > a')[0]
    localBeatifulSoup.select('.tang > ul  > a')[0]
    localBeatifulSoup.select('.tang > ul  > a')[0]
    # 如何获取标签之间的数据
    localBeatifulSoup.select('.tang > ul  > a')[0].getText
    # soup.a.text string getText
    # - text,getText 可以获取某一个标签中的所有文本内容
    # - string 只可以获取该标签下的直系的文本内容
    # 获取标签中属性值
    # soup.a['href']
    localBeatifulSoup.a['href']

# 网络获取html 加载到BeautifulSoup对象中
url = ''
head = {}
page_text = requests.get(url=url, headers=head)
net_bs4Soup = BeautifulSoup(page_text)
#   提供用于解析数据的的方法和属性

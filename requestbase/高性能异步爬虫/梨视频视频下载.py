import math
import random

import requests
from multiprocessing.dummy import Pool
from lxml import etree
import re
import json
import os


class MyClass:
    def __init__(self, url, name):
        self.url = url
        self.name = name


def replace_func(match_obj):
    return match_obj.group(1) + 'aaa' + match_obj.group(3)


reg = r'(.*\/)(\d+-)(.*)'

url = 'https://www.pearvideo.com/category_1'
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

mainPage = requests.get(url=url, headers=header)
mainPageData = mainPage.text
pageEtree = etree.HTML(mainPageData)
targetLi = pageEtree.xpath('//*[@id="listvideoListUl"]/li')
HOST_DOMAIN = 'https://www.pearvideo.com/'
cookie = requests.session()
my_set = []
for li in targetLi:
    fileName = li.xpath('.//div[@class="vervideo-title"]/text()')
    print(fileName[0])
    name = fileName[0]
    resource_address = li.xpath('.//div[@class="vervideo-bd"]/a/@href')
    print(resource_address)
    videoUrl = HOST_DOMAIN + resource_address[0]
    print(videoUrl)
    # 进入详情页获取视频资源地址
    videoDetailPage = cookie.get(url=videoUrl, headers=header)
    videoMp4Url = 'https://www.pearvideo.com/videoStatus.jsp?mrd=0.913413241341&contId=' + resource_address[0].replace(
        'video_', '')
    print(videoMp4Url)
    header_ajax = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Referer': videoUrl
    }
    videoDetailJson = cookie.get(url=videoMp4Url, headers=header_ajax).json()
    # print(videoDetailJson)
    # print(videoDetailJson['resultCode'])
    # print(videoDetailJson['videoInfo'])
    # print(videoDetailJson['videoInfo']['videos'])
    print(videoDetailJson['videoInfo']['videos']['srcUrl'])
    mediaUrl = videoDetailJson['videoInfo']['videos']['srcUrl']
    middleStr = 'cont-' + resource_address[0].replace('video_', '')
    new_url = re.sub(reg, replace_func, mediaUrl)
    downloadUrl = new_url.replace('aaa', middleStr + '-')
    resourceAddress = MyClass(name=name, url=downloadUrl)
    my_set.append(resourceAddress)


def getPage(obj):
    if not os.path.exists('./liMp4Lib'):
        os.mkdir('./liMp4Lib')
    print(obj.name, "正在下载...")
    downloadsUrl = obj.url
    fileName = obj.name
    print(fileName, downloadsUrl)
    mp4Data = requests.get(url=downloadsUrl, headers=header).content
    path = './liMp4Lib/' + obj.name + '.mp4'
    with open(path, 'wb') as fb:
        fb.write(mp4Data)
    print(obj.name, '下载完毕！')


pool = Pool(len(li))
pool.map(getPage, my_set)




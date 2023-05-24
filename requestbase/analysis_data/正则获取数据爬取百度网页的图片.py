import random
import re
import uuid

import requests
import json
import re
import os

if __name__ == '__main__':
    if not os.path.exists('./baiduSKLib'):
        os.mkdir('./baiduSKLib')

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E6%95%B0%E9%93%BE%E7%A7%91%E6%8A%80'
    baiduUrl = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E6%95%B0%E9%93%BE%E7%A7%91%E6%8A%80&x_bfe_rqs=03E8000000000000000008&x_bfe_tjscore=0.100000&tngroupname=organic&newVideo=12&goods_entry_switch=1&pn={}'
    dic = ['0', '10', '20']
    for pageNum in dic:
        new_url = baiduUrl.format(pageNum)
        print(new_url)
        page_text = requests.get(url=new_url, headers=header).text
        # print(page_text)
        # 将页面中的图片进行解析
    ex = '<div[^>]*>\s*<span[^>]*><\/span>\s*<img[^>]*\ssrc\s*=\s*"([^"]*)"[^>]*>\s*<\/div>'
    list_img = re.findall(ex, page_text, re.S)
    print(list_img)
# # 遍历列表
for src in list_img:
    # 拼接完整的url
    src = 'https:' + src
    image = requests.get(url=src, headers=header).content
    # 生成图片图标
    fileName = uuid.uuid4()
    imagePath = './baiduSKLib/' + fileName
    with open(imagePath, 'wb') as fb:
        fb.write(image)
        print(fileName + "下载成功")
# https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E6%95%B0%E9%93%BE%E7%A7%91%E6%8A%80&x_bfe_rqs=03E8000000000000000008                &x_bfe_tjscore=0.100000&tngroupname=organic&newVideo=12&goods_entry_switch=1&pn=0
# https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E6%95%B0%E9%93%BE%E7%A7%91%E6%8A%80&x_bfe_rqs=03E80000000000000000080000000000000008&x_bfe_tjscore=0.100000&tngroupname=organic&newVideo=12&goods_entry_switch=1&pn=10
# https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E6%95%B0%E9%93%BE%E7%A7%91%E6%8A%80&x_bfe_rqs=03E8000000000000000008                &x_bfe_tjscore=0.100000&tngroupname=organic&newVideo=12&goods_entry_switch=1&pn=20

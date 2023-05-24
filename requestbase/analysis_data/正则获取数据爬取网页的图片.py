import re

import requests
import json
import re
import os

if __name__ == '__main__':
    if not os.path.exists('./qutoutiaoLib'):
        os.mkdir('./qutoutiaoLib')

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    url = 'http://www.qutoutiao.net/about.html'
    page_text = requests.get(url=url, headers=header).text
    # 将页面中的图片进行解析
    # div display  div list  div div_img
    # <div class="div_img"><img src="//cdn-qukan.1sapp.com/qukan/qtt_website/midu.png" alt=""></div>
ex = '<div[^>]*>\s*<img[^>]*\ssrc\s*=\s*"([^"]*)"[^>]*>\s*</div>'
list_img = re.findall(ex, page_text, re.S)
print(list_img)

# 遍历列表
for src in list_img:
    # 拼接完整的url
    src = 'https:' + src
    image = requests.get(url=src, headers=header).content
    # 生成图片图标
    fileName = src.split('/')[-1]
    imagePath = './qutoutiaoLib/' + fileName
    with open(imagePath, 'wb') as fb:
        fb.write(image)
        print(fileName+"下载成功")

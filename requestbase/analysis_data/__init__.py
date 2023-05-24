# 查询某个网页图片
import requests
import json
if __name__ == '__main__':
 header ={
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
 }
 img_url='http://cdn-qukan.1sapp.com/qukan/qtt_website/midu.png'
 # 返回的二进制的图片数据
 # text 字符串、content 二进制 json json对象
 response =requests.get(url=img_url).content
 with open ('./midu.png','wb') as fb:
  fb.write(response)
  print("图片下载完毕！")

# requests模块
  # urllib
  # requests模块
# requests 模块 ，python 中原生中基于网络请求的模块，功能非常强大
# 作用:模拟浏览器请求
# 如何使用
# ① 指定url
# ② 发起请求
# ③ 获取响应内容
# ④ 持久化存储数据。
# 环境pop install

# 爬取搜狗首页数据
import  requests;
if __name__ == '__main__':
  url= "https://www.baidu.com/"
# 发起请求
  response=requests.get(url=url)
# 请求成功后会有一个对象
  page_text =response.text;
  print(page_text)
# 存储
  with open('./baidu.html','w',encoding='utf-8') as fp:
      fp.write(page_text)
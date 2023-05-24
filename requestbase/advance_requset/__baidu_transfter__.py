# need  破解百度翻译
import requests
import json
if __name__ == '__main__':
 header ={
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
 }
 # 指定url
 post_url='https://fanyi.baidu.com/sug'
 word = input("请输入要翻译的中文：")
 post_data ={
  'kw':word
 }

 # 请求参数
 response=requests.post(url=post_url,data=post_data,headers=header)
 # json 返回是一个json对象
 jsonData= response.json()
 print(jsonData)
 fp= open('./dog.json','w',encoding='utf-8')
 json.dump(jsonData,fp=fp,ensure_ascii=False)

 print("数据翻译结束")

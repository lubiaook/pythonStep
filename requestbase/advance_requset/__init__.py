# need 简易的网络采集器： 爬取搜狗指定词条对应的搜索结果页面。
# UA伪装 User-Agent
# 门户网站服务器会检测请你去载体的身份标志，如果检测到为某个浏览器身份，如果检测到不是基于某一种楼篮球，则表示该服务器为不正常的请求（爬虫），可能拒绝访问。
# 所以爬虫程序需要做UA伪装，
# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
import requests
if __name__ == '__main__':
    # url='https://www.sogou.com/'
    # UA伪装
    header ={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    # 找到对应的url
    url = 'https://www.sogou.com/web'
    kw = input('enter a key word : ')
    requestParms = {
        'query': kw
    }
    response = requests.get(url=url, params=requestParms,headers=header)
    page_text=response.text;
    print(page_text)
    fileName=kw+'.html'
    print(fileName)
    with open (fileName,'w',encoding='utf-8') as fp:
     fp.write(page_text)
     fp.close();
     print(fileName,'保存成功')

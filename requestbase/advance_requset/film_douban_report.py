# need 爬取豆瓣电影分类排行榜
# UA伪装 User-Agent
import requests
if __name__ == '__main__':
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

# need 爬取豆瓣电影分类排行榜
# UA伪装 User-Agent
import requests

if __name__ == '__main__':
    # UA伪装
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    url = 'https://www.sogou.com/web'
    id_list = []
    # 参数封装  分页
    for page in range(1, 6):
        page = str(page)
        data = {
            'on': 'true',
            'page': page,
            'pageSize': '15',
            'productName': '',
            'conditionType': '1',
            'applyName': '',
            'applysn': '',
        }
        json_ids = requests.get(url=url, params=data, headers=header)
        for dic in json_ids['list']:
            id_list.append(dic['ID'])

    #  获取企业详情
    post_url_detail=''

    # 找到对应的url
    kw = input('enter a key word : ')
    requestParms = {
        'query': kw
    }
    response = requests.get(url=url, params=requestParms, headers=header)
    page_text = response.text;
    print(page_text)
    fileName = kw + '.html'
    print(fileName)
    with open(fileName, 'w', encoding='utf-8') as fp:
        fp.write(page_text)
        fp.close()
        print(fileName, '保存成功')

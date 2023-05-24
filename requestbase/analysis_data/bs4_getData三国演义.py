import requests
from bs4 import BeautifulSoup
import os

if __name__ == '__main__':
    if not os.path.exists('./sanguoyanyiLib'):
        os.mkdir('./sanguoyanyiLib')

    url = 'http://www.shicimingju.com/book/sanguoyanyi.html'
    perxUrl = 'http://www.shicimingju.com/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=header)
    response.encoding = 'GBK'
    response.encoding = 'utf-8'
    page_text = response.text
    print(page_text)
    net_bs4Soup = BeautifulSoup(page_text, 'lxml')
    # print(net_bs4Soup)
    li_list = net_bs4Soup.select('.book-mulu > ul > li')
    fp = open('./sannguo.txt', 'w', encoding='utf-8')
    for li in li_list:
        # < a href = "/book/sanguoyanyi/1.html" > 第一回·宴桃园豪杰三结义 斩黄巾英雄首立功 < / a >
        # print(li['href'])
        # print(li.a['href'])
        # print(li.string.encode(encoding='utf-8'))
        title = li.a.string
        detailUrl = perxUrl + li.a['href']
        detailTextBookResponse = requests.get(detailUrl, headers=header)
        detailTextBookResponse.encoding = 'GBK'
        detailTextBookResponse.encoding = 'utf-8'
        detailSoup = BeautifulSoup(detailTextBookResponse.text, 'lxml')
        detailSoupDetailResponse = detailSoup.find('div', class_='chapter_content')
        detailSoupDetail = detailSoupDetailResponse.text
        # txtPath='./sanguoyanyiLib/'+title+".txt"
        # with open(txtPath,'w',encoding='utf-8') as fb:
        #     fb.write(detailSoupDetail)
        fp.write(title + " : " + detailSoupDetail + '\n')
        print(title, '爬取成功！')

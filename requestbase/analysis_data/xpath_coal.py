import requests
from lxml import etree
import os

if __name__ == '__main__':
    # 查看是否有此目录
    if not os.path.exists('./resumeLib'):
        os.mkdir('./resumeLib')
    # host = 'https://sc.chinaz.com/'
    url = 'https://sc.chinaz.com/jianli/free.html'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=header)
    # 解决乱码问题
    response.encoding = 'GBK'
    response.encoding = 'utf-8'
    # print(response.text)
    responseEtree = etree.HTML(response.text)
    aSpanXpaths = responseEtree.xpath('//div[@class="box col3 ws_block"]/a')
    # print(aSpanXpaths)
    for aSpan in aSpanXpaths:
        url = aSpan.xpath('./@href')
        fileName = aSpan.xpath('./img/@alt')[0]
        # print(fileName)
        downUrlDetail = url[0]
        # print(downUrlDetail)
        downPageResponse = requests.get(url=downUrlDetail, headers=header)
        downPageResponse.encoding = 'GBK'
        downPageResponse.encoding = 'utf-8'
        # print(downPageResponse.text)
        # 将资源地址放在etree对象
        downLoadUrl = etree.HTML(downPageResponse.text)
        # rarDownloadUrl = downLoadUrl.xpath('//url[@class="clearfix"]/li')
        rarDownloadLiUrl = downLoadUrl.xpath('//div[@class="down_wrap"]//li/a/@href')[0]
        # print(rarDownloadLiUrl)
        resumeRarResponse = requests.get(url=rarDownloadLiUrl, headers=header)
        #  todo 获取下载文件的问你件后缀拼接
        with open('./resumeLib/' + fileName + '.rar', 'wb') as fb:
            fb.write(resumeRarResponse.content)
            print(fileName, "简历下载完毕！")

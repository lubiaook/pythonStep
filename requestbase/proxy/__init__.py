# 代理伪装IP
import requests
from lxml import etree

if __name__ == '__main__':
    url = 'https://ip.900cha.com/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    # ip_page = requests.get(url=url, headers=header)

    ip_page = requests.get(url=url, headers=header, proxies={"http": '58.45.135.136:8911'})
    ip_page.encoding = "GBK"
    ip_page.encoding = 'utf-8'
    ipPageText = ip_page.text

    # print(ip_page.xpath('//div[@class="c-span21 c-span-last op-ip-detail"]//span//text()'))
    #  print(ipPageText.xpath('//*[@id="1"]/div[1]/div[1]/div[2]/table/tbody/tr/td/span'))
    # fitter= ip_page.xpath('//*[@id="1"]/div[1]/div[1]/div[2]')
    # print(fitter)
    with open('./ip.html', 'w', encoding='utf-8') as wb:
        wb.write(ipPageText)
        wb.close()

    xpathData = etree.HTML(ipPageText)
    # print(ipPageText)
    print(xpathData.xpath('/html/body/div/div/div/div[1]/div[1]/h3/text()')[0])

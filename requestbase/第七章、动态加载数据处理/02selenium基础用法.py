from selenium import webdriver
from lxml import etree
from time import sleep

# 实例化chromWeb(传入浏览器对象)
chromWeb = webdriver.Chrome('./chromedriver')
# 编写基于浏览器的代码
chromWeb.get('http://www.jiaolianwang.com/index.php?controller=site&action=article')

mainPage = chromWeb.page_source
etreeMainPage = etree.HTML(mainPage)

li_list = etreeMainPage.xpath('//div[@class="y-newslist-right"]//li')
print(li_list)
for li in li_list:
    # print(li.xpath('.//text()'))
    print(li.xpath('./a/text()')[0])





sleep(5)
chromWeb.quit()

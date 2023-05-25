from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

bro = webdriver.Chrome(executable_path='./chromedriver')
url = ''
bro.get(url=url)
pageData = bro.page_source
# 如果定位的标签在iframe中必须通过 switch_to定位标签
bro.switch_to.frame('iframeId')
div = bro.find_element(By.Class, 'class')

# 定义作用联
actionLink = ActionChains(bro)
# 动作链持有div
actionLink.click_and_hold(div)
for i in range(5):
    # move_by_offset()
    # perform() 立即执行
    actionLink.move_by_offset(17, 0).perform()
# 释放动作链
actionLink.release()

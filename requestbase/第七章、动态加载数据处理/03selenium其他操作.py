from selenium import webdriver
from time import sleep
from lxml import etree
from selenium.webdriver.common.by import By

bro = webdriver.Chrome(executable_path='./chromedriver')
bro.get('https://www.taobao.com')
pageData = bro.page_source
etreePageData = etree.HTML(pageData)
# element = driver.find_element(By.ID, 'foo')
# 执行一组js程序
bro.execute_script('window.scroll(0,document.body.scrollHeight)')
sleep(2)
## 输入框
searchInputText = bro.find_element(By.ID, 'q')
searchInputText.send_keys("婴儿喂 神器")
searchInputText = bro.find_element(By.ID, 'q')
## 按钮
submitBtn = bro.find_element(By.CLASS_NAME, 'btn-search')
submitBtn.click()

# //*[@id="q"]
sleep(20)
bro.quit()

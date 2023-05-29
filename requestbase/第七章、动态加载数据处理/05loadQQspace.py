from selenium import webdriver
from time import sleep

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions

url = 'https://qzone.qq.com/'
# bro = webdriver.Chrome('./chromedriver')
# 创建ChromeDriver服务对象
chromedriver_path = '/path/to/chromedriver'
service = Service(executable_path=chromedriver_path)

# 创建Chrome浏览器实例
options = webdriver.ChromeOptions()
# chromeOption=Options()
## start 设置无可视化页面
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
## end 设置无可视化页面
### 如何规selenium被服务器检测
# options= ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

bro = webdriver.Chrome(service=service, options=options)
bro.get(url)
bro.switch_to.frame('login_frame')
switchBtn = bro.find_element(By.ID, 'switcher_plogin')
switchBtn.click()

sleep(2)
userNameInput = bro.find_element(By.ID, 'u')
userNameInput.send_keys('742811570')
sleep(2)
userPwdInput = bro.find_element(By.ID, 'p')
userPwdInput.send_keys('123321Yuyu!')

sleep(5)
submitBtn = bro.find_element(By.ID, 'login_button')
submitBtn.click()

bro.execute_script('window.scroll(0,document.body.scrollHeight)')
sleep(5)
bro.execute_script('window.scroll(0,document.body.scrollHeight)')
sleep(5)
bro.execute_script('window.scroll(0,document.body.scrollHeight)')
sleep(5)
# bro.quit()

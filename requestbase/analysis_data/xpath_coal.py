from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)


@app.route('/get_data/<page>', methods=['GET'])
def get_data(page):
    url = "https://quote.eastmoney.com/qihuo/" + page
    print(url)
    # 设置 Chrome 驱动器路径
    chrome_driver_path = './chromedriver'
    # 创建 Chrome 选项
    options = webdriver.ChromeOptions()
    ## start 设置无可视化页面
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 创建 Chrome 服务
    service = Service(chrome_driver_path)
    # 创建 Chrome 驱动器
    driver = webdriver.Chrome(service=service, options=options)
    # 打开页面
    driver.get(url)
    # 使用 XPath 获取元素值
    currentElement = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[8]/div[1]/div/div[1]')
    dayOpenElement = driver.find_element(By.XPATH,
                                         '//*[@id="app"]/div/div/div[8]/div[2]/div/table/tbody/tr[1]/td[1]/span/span')
    yesterdayEndOpenElement = driver.find_element(By.XPATH,
                                                  '//*[@id="app"]/div/div/div[8]/div[2]/div/table/tbody/tr[2]/td[1]/span/span')
    data = currentElement.text
    print("今开盘价：" + dayOpenElement.text)
    print("昨日收盘价：" + yesterdayEndOpenElement.text)
    data = {
        'current': currentElement.text,
        'day_open': dayOpenElement.text,
        'yesterday_end_open': yesterdayEndOpenElement.text
    }
    # 关闭浏览器
    driver.quit()

    # 返回数据给调用方
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run(debug=True)

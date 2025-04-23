import json
import time
from urllib.parse import urlencode

import requests
from flask import Flask, jsonify
from lxml import html
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
from requestbase.analysis_data.prod_select_request import proxies

app = Flask(__name__)

valid_pages_oil = [];
valid_pages_doupo = [];


def get_data_for_dict(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        # # 解析HTML
        # doc = pq(response.text)
        # # 找到表格
        # table = doc('.dataArea')
        # # 提取表格行
        # rows = table.find('tr')
        # # 遍历表格行，提取第二列数据并过滤
        # filtered_data = []
        # for row in rows.items():
        #     cols = row.find('td')
        #     if len(cols) > 1:  # 确保有足够的列
        #         second_col_text = cols.eq(1).text().strip()
        #         if second_col_text.endswith(('01', '05', '09')):
        #             filtered_data.append(second_col_text)

        # 解析HTML内容
        tree = html.fromstring(response.content)
        # 找到表格
        table = tree.find_class('dataArea')
        if not table:
            raise ValueError('Table not found')
        # 提取表格行
        rows = table[0].xpath('.//tr')
        # 遍历表格行，提取第二列数据并过滤
        filtered_data = []
        for row in rows[1:]:  # 跳过表头行
            cols = row.xpath('.//td')
            if len(cols) > 1:  # 确保有足够的列
                second_col_text = cols[1].text_content().strip()
                if second_col_text.endswith(('01', '05', '09')):
                    filtered_data.append(second_col_text)

        # 打印过滤后的数据
        for data in filtered_data:
            print(data)
        data = {
            'status': 1,
            'options': filtered_data
        }
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        data = {'status': 0, 'error': str(e)}
    except Exception as e:
        # 处理其他异常
        data = {'status': 0, 'error': str(e)}
    return data


def get_data_from_page(url):
    try:
        # response = requests.get(url, proxies=proxies)
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        # 提取 JSON 数据
        # data_str = response.text
        # start_index = data_str.index('(') + 1
        # end_index = data_str.rindex(')')

        # json_data = json.loads(data_str[start_index:end_index])
        # qt_data = json_data.get("qt", {})
        #
        response_text = response.text
        start_index = response_text.index('(') + 1
        end_index = response_text.rindex(')')
        json_str = response_text[start_index:end_index]
        json_data = json.loads(json_str)

        qt_data = json_data.get("qt", {})
        # 过滤所需字段
        filtered_data = {
            'current': qt_data.get('p'),
            'cnName': qt_data.get('name'),
            'enName': qt_data.get('dm')
        }

        return {
            'status': 1,
            'data': filtered_data
        }
    except requests.RequestException as e:
        return {
            'status': 0,
            'error': str(e)
        }


@app.route('/get_dict/<page>', methods=['GET'])
def get_dict(page):
    url = 'http://www.dce.com.cn/publicweb/businessguidelines/queryContractInfoVariety.html?variety='
    if page == 'qihuo_doupo':
        print(url)
        data = get_data_for_dict(url + "m")
        if data['status'] == 1:
            global valid_pages_doupo
            valid_pages_doupo = data['options']
            print(valid_pages_doupo)
    elif page == 'qihuo_oil':
        data = get_data_for_dict(url + "y")
        if data['status'] == 1:
            global valid_pages_oil
            valid_pages_oil = data['options']
            print(valid_pages_oil)
    else:
        data = valid_pages_oil
    return jsonify({'data': data})


@app.route('/get_data/<key>/<type>', methods=['GET'])
def get_data(key, type):
    # 获取集合
    if type == 'doupo':
        get_dict("qihuo_doupo");
        if key not in valid_pages_doupo:
            return jsonify({'error': 'Invalid page value. Must be one of: {}'.format(valid_pages_doupo)}), 400
    elif type == 'oil':
        get_dict("qihuo_oil");
        if key not in valid_pages_oil:
            return jsonify({'error': 'Invalid page value. Must be one of: {}'.format(valid_pages_oil)}), 400
    else:
        return {'status': 0,
                'error': 'Element not found'}

    base_url = 'https://futsseapi.eastmoney.com/static/114_' + key + '_qt'
    callbackName = 'jQuery351010572162692011666_' + str(current_timestamp)
    params = {
        "callbackName": callbackName,
        "orderBy": "zdf",
        "sort": "desc",
        "pageSize": 10,
        "pageIndex": 0,
        "field": "name,dm,sc,p,zsjd,zdf",
        "_": current_timestamp
    }
    url = build_url(base_url, params)
    print(url)
    data = get_data_from_page(url)
    return jsonify(data)


@app.route('/get_data/dict/<type>', methods=['GET'])
def get_data_for_dictAA(type):
    url = 'http://www.dce.com.cn/publicweb/businessguidelines/queryContractInfoVariety.html?variety=' + type
    data = get_data_for_dict(url)
    return jsonify({'data': data})


@app.route('/get_money/forex/<type>', methods=['GET'])
def get_data_for_forex_money(type):
    if type == '':
        url = 'https://finance.pae.baidu.com/vapi/v1/getquotation?group=huilv_minute&need_reverse_real=1&code=USDCNH&finClientType=pc'
    else:
        url = 'https://finance.pae.baidu.com/vapi/v1/getquotation?group=huilv_minute&need_reverse_real=1&code=' + type + '&finClientType=pc'
    data = get_data_for_forex_money_A(url)
    return jsonify({'data': data})


# 获取人民币离案
def get_data_for_forex_money_A_V2(url):
    try:
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://finance.pae.baidu.com"
            # Add other necessary headers here
        }
        response = requests.get(url=url, headers=header)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        if response.status_code == 200 and data['ResultCode'] == 0:
            current_price = data['Result']['cur']['price']
            data = {
                'status': 1,
                'current': float(current_price)
            }
        else:
            data = {
                'status': 0,
                'error': '接口请求失败' + response.status_code
            }
    except requests.RequestException as e:
        return {
            'status': 0,
            'error': str(e)
        }
    return data


# 获取人民币离案
def get_data_for_forex_money_A(url):
    url = 'https://finance.sina.com.cn/money/forex/hq/USDCNH.shtml'
    try:
        chrome_driver_path = './chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
        driver.get(url)
        currentElement = driver.find_element(By.XPATH, '//*[@id="quoteWrap"]/div[1]/div/h5')
        data = {
            'status': 1,
            'current': currentElement.text
        }
        driver.quit()
    except NoSuchElementException as e:
        # 处理元素未找到异常
        data = {'status': 0,
                'error': 'Element not found'}
    except Exception as e:
        # 处理其他异常
        data = {'status': 0, 'error': str(e)}
    return data


def build_url(base_url, params):
    """
    构建带参数的完整 URL。

    :param base_url: 基础 URL
    :param params: 包含参数及其值的字典
    :return: 带参数的完整 URL
    """
    query_string = urlencode(params)
    full_url = f"{base_url}?{query_string}"
    return full_url


# 获取当前时间戳
current_timestamp = int(time.time() * 1000)


@app.route('/get_qihuo/<type>', methods=['GET'])
def get_qihuo(type):
    base_url = "https://futsseapi.eastmoney.com/list/variety/114/4"
    if type == 'qihuo_oil':
        base_url = "https://futsseapi.eastmoney.com/list/variety/114/5"
    elif type == 'qihuo_doupo':
        base_url = "https://futsseapi.eastmoney.com/list/variety/114/4"

    else:
        return {
            'status': 0,
            'error': str("请求参数异常：qihuo_oil,qihuo_doupo")
        }

    # URL 参数
    callbackName = 'jQuery351031842976686538793_' + str(current_timestamp)
    params = {
        "callbackName": callbackName,
        "orderBy": "zdf",
        "sort": "asc",
        "pageSize": 10,
        "pageIndex": 0,
        "field": "name,dm,sc,p,zsjd,zdf",
        "_": current_timestamp
    }

    # 构建完整的 URL
    url = build_url(base_url, params)
    print(url)
    data = get_filtered_data(url)
    return jsonify({'data': data})


def get_filtered_data(url, proxies=None):
    try:
        # response = requests.get(url, proxies=proxies)
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        # 提取 JSON 数据
        data_str = response.text
        start_index = data_str.index('(') + 1
        end_index = data_str.rindex(')')
        json_data = json.loads(data_str[start_index:end_index])

        # 过滤 dm 字段以 '09'、'03'、'01' 结尾的数据，并获取相应的 p 值
        filtered_data = [{'cnName': item['dm'], 'current': item['p']} for item in json_data['list'] if
                         item['dm'].endswith(('09', '05', '01'))]

        return {
            'status': 1,
            'options': filtered_data
        }
    except requests.RequestException as e:
        return {
            'status': 0,
            'error': str(e)
        }


@app.route('/get_ship_location/<code>', methods=['GET'])
def getShipLocation(code):
    try:
        chrome_driver_path = './chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
        driver.get('https://www.shipxy.com/')

        # 等待页面加载（如果需要的话，可以使用显式等待）
        #time.sleep(1)  # 这里使用简单的time.sleep作为示例，实际应使用WebDriverWait

        # 通过XPath找到输入框并输入内容
        input_box = driver.find_element(By.XPATH, '//*[@id="txtKey"]')
        input_box.send_keys(code)
        # 通过XPath找到并点击按钮
        search_button = driver.find_element(By.XPATH, '//*[@id="searchBtn"]')
        search_button.click()
        time.sleep(1)
        # 等待搜索结果加载（如果需要的话，可以再次使用显式等待）
        #close_button =driver.find_element(By.XPATH,'//*[@id="shipinfoTitle"]/div[1]/a/img');
        # close_button.click()
        si_lat = driver.find_element(By.XPATH,'//*[@id="si__lat"]')
        si_lon = driver.find_element(By.XPATH,'//*[@id="si__lon"]')
        # 进行其他操作或打印页面内容（可选）
        data = {
            'status': 1,
            'si_lat': si_lat.text,
            'si_lon': si_lon.text
        }

        driver.quit()
    except NoSuchElementException as e:
        # 处理元素未找到异常
          data = {'status': 0,
                'error': 'Element not found'}
    except Exception as e:
        # 处理其他异常
          data = {'status': 0, 'error': str(e)}
    return data;


if __name__ == '__main__':
    app.run(debug=True)

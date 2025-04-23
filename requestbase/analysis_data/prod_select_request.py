import json
import time
from urllib.parse import urlencode

from flask import Flask, jsonify
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from pyquery import PyQuery as pq

app = Flask(__name__)

valid_pages_oil = [];
valid_pages_doupo = [];


def get_data_for_dict(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析HTML
        doc = pq(response.text)

        # 找到表格
        table = doc('.dataArea')

        # 提取表格行
        rows = table.find('tr')

        # 遍历表格行，提取第二列数据并过滤
        filtered_data = []
        for row in rows.items():
            cols = row.find('td')
            if len(cols) > 1:  # 确保有足够的列
                second_col_text = cols.eq(1).text().strip()
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


@app.route('/get_data/dict/<type>', methods=['GET'])
def get_data_for_dictAA(type):
    url = 'http://www.dce.com.cn/publicweb/businessguidelines/queryContractInfoVariety.html?variety=' + type
    data = get_data_for_dict(url)
    return jsonify({'data': data})


@app.route('/get_money/forex/<type>', methods=['GET'])
def get_data_for_forex_money(type):
    url = 'https://quote.eastmoney.com/qihuo/m2409.html'
    data = get_data_for_forex_money_A(url)
    return jsonify({'data': data})


def get_data_for_forex_money_A(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析HTML
        doc = pq(response.text)

        # 查找元素
        current_element = doc('#app > div > div > div:nth-child(8) > div:nth-child(1) > div > div:nth-child(1)')
        cn_name = doc('#app > div > div > div:nth-child(7) > div > div:nth-child(1) > span:nth-child(1)')
        en_name = doc('#app > div > div > div:nth-child(7) > div > div:nth-child(1) > span:nth-child(2)')
        img_source = doc(
            '#app > div > div > div.layout_sm > div.layout_sm_sider > div:nth-child(1) > div.sidertabbox_c.false > div > div:nth-child(1) > a > img')
        print('输出图片路径' + img_source.text().strip())
        if current_element and cn_name and en_name:
            data = {
                'status': 1,
                'current': current_element.text().strip(),
                'enName': en_name.text().strip(),
                'cnName': cn_name.text().strip()
            }
        else:
            data = {
                'status': 0,
                'error': 'Element not found'
            }
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        data = {'status': 0, 'error': str(e)}
    except Exception as e:
        # 处理其他异常
        data = {'status': 0, 'error': str(e)}

    return data


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
        "sort": "desc",
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


# 设置代理
proxies = {
    "http": "http://your_http_proxy_address:port",
    "https": "https://your_https_proxy_address:port"
}


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


@app.route('/get_data/<type>/oil', methods=['GET'])
def get_data_oil(type):
    base_url = 'https://futsseapi.eastmoney.com/static/114_' + type + '_qt'
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
    data = get_qihuo_detail(url)
    return data;


def get_qihuo_detail(url, proxies=None):
    # https: // futsseapi.eastmoney.com / static / 114_y2409_qt?callbackName = jQuery351010572162692011666_1716877142747 & field = name, sc, dm, p, zsjd, zdf, zde, utime, o, zjsj, qrspj, h, l, mrj, mcj, vol, cclbh, zt, dt, np, wp, ccl, rz, cje, mcl, mrl, jjsj, j, lb, zf & token = 1101
    # ffec61617c99be287c1bec3085ff & _ = 1716877142748
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # 检查请求是否成功
        # 提取 JSON 数据
        data_str = response.text
        start_index = data_str.index('(') + 1
        end_index = data_str.rindex(')')
        json_data = json.loads(data_str[start_index:end_index])
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


if __name__ == '__main__':
    app.run(debug=True)

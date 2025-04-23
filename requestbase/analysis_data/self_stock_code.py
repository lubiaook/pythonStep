# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
import requests
import operator
from apscheduler.schedulers.blocking import BlockingScheduler
import json
import time as time_module

array_stocks = ["600292","002094","000601"]

key_map = {
    "600292":"远达环保",
            "000601":"韶能股份",
            "000524":"岭南控股",
            "002094":"青岛金王",
            "601086":"国芳集团"
}

key_price ={
	"300139":"涨停出",
    "600292": "关注入",
    "000899": "关注入",
            "000601":"关注出",
    "000524": "关注入",
    "002094": "关注入",
    "601086": "关注入"
}


def sent_ding_msg(request_body):
    token = get_ding_token()
    try:
        post_sent_msg_url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=' + token
        # print(post_sent_msg_url)
        # request_body = {
        #     "agent_id": 3123423208,
        #     "msg": {
        #         "msgtype": "text",
        #         "text": {
        #             "content": msg
        #         }
        #     },
        #     "userid_list": "06490107591216996"
        # }
        post_data = requests.post(url=post_sent_msg_url, json=request_body)

        post_data.raise_for_status()  # 检查请求是否成功

        print(post_data.text)
    except Exception as e:
        print(e)
    return ""


def get_ding_token():
    appkey = 'ding6at3fmyyvny2rldg'
    appsecret = 'c4_uzBWoS6CVfSIjU2775k3XOE2WmjD7YT4S0pRJlpC6bm5YLj4EllhAAvbrzXfx'
    url = 'https://oapi.dingtalk.com/gettoken?appkey=' + appkey + '&appsecret=' + appsecret
    # print(url)
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
    # 提取 JSON 数据
    data_str = response.text
    data = json.loads(data_str)
    token = data['access_token']
    print(token)
    return token


def build_msg(rate, code, name, current_price, base_price, time):
    title = ''
    if rate > 0:
        title = f'👏🏻{name} 涨了 {rate}%'
    else:
        title = f'⚠️{name} 跌了 {rate}%'

    data = {
        "agent_id": 3123423208,
        "userid_list": "06490107591216996",
        "msg": {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"#    \n   ### ({code}) {title}   \n * 当前价格：***{current_price}***    \n  * 成本价格: ***{base_price}***    \n * 日期： {time}  \n"

            }
        }
    }
    return data


def compare_stock_code(code):
    company_name = key_map.get(code, code)
    # 请求数据
    url = "https://finance.pae.baidu.com/vapi/v1/getquotation?all=1&pointType=string&group=quotation_fiveday_ab&market_type=ab&new_Format=1&name=" + company_name + "&finClientType=pc&query=" + code + "&code=" + code
    print(url)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://finance.pae.baidu.com"
    }
    response = requests.get(url=url, headers=header)
    data = response.json()
    # print(data)
    # 提取 marketData
    market_data = data['Result']['newMarketData']['marketData']
    market_date_time = data['Result']['update']['text']

    # 获取倒数第一、二个数据
    last_data = market_data[-1]['p']
    second_last_data = market_data[-2]['p']

    # 分割并获取最后一个部分
    last_data_parts = last_data.split(';')
    second_last_data_parts = second_last_data.split(';')

    last_data_last_part = last_data_parts[-1]
    second_last_data_last_part = second_last_data_parts[-1]
    # print("今天：",last_data_last_part)
    # print("昨天：",second_last_data_last_part)

    # 分割最后一个部分并获取最后一个数据值
    last_data_last_value = last_data_last_part.split(',')
    second_last_data_last_value = second_last_data_last_part.split(',')

    date_today = last_data_last_value[1]
    today_price = last_data_last_value[2]

    date_last = second_last_data_last_value[1]

    last_price = second_last_data_last_value[2]

    num1 = operator.sub(float(today_price), float(last_price))
    rate = operator.truediv(num1, float(last_price))
    k = round(operator.mul(rate, 100), 2)
    company_name = key_map.get(code, code)
    base_price = key_price.get(code, code)
    msg = ''
    if rate > 0.02:
        msg = f'{company_name}({code}), 当前价格{today_price} 涨了,涨幅: {k}%%'
        if 0.02 < rate < 0.03:
            msg = f'{company_name}({code}), 当前价格{today_price} 涨了超过 2%，涨幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif 0.03 <= rate < 0.04:
            msg = f'{company_name}({code}), 当前价格{today_price} 涨了超过 3%，涨幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif 0.04 <= rate < 0.05:
            msg = f'{company_name}({code}), 当前价格{today_price} 涨了超过 4%，涨幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif 0.05 <= rate < 0.06:
            msg = f'{company_name}({code}), 当前价格{today_price} 涨了超过 5%，涨幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif 0.06 <= rate < 0.07:
            msg = f'{company_name}({code}), 当前价格{today_price} 涨了超过 6%，涨幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif 0.07 <= rate < 0.08:
            msg = f'{company_name}({code}), 当前价格{today_price} 涨了超过 7%，涨幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif 0.08 <= rate < 0.09:
            msg = f'{company_name}({code}), 当前价格{today_price} 涨了超过 8%，涨幅: {k}%%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif rate >= 0.09:
            msg = f'{company_name}({code}), 当前价格{today_price} 涨了超过 9%，涨幅: {k}%%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        print(msg)
    elif rate < 0:
        msg = f'{company_name}({code}), 当前价格{today_price} 跌了 ,跌幅: {k}%%,({current_timestamp})'
        if -0.03 > rate > -0.04:
            msg = f'{company_name}({code}), 当前价格{today_price} 跌了超过 3%，跌幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif -0.04 >= rate > -0.05:
            msg = f'{company_name}({code}), 当前价格{today_price} 跌了超过 4%，跌幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif -0.05 >= rate > -0.06:
            msg = f'{company_name}({code}), 当前价格{today_price} 跌了超过 5%，跌幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif -0.06 >= rate > -0.07:
            msg = f'{company_name}({code}), 当前价格{today_price} 跌了超过 6%，跌幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif -0.07 >= rate > -0.08:
            msg = f'{company_name}({code}), 当前价格{today_price} 跌了超过 7%，跌幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        elif rate <= -0.08:
            msg = f'{company_name}({code}), 当前价格{today_price} 跌了超过 8%，跌幅: {k}%,({current_timestamp})'
            data = build_msg(k, code, company_name, current_price=today_price, base_price=base_price,
                             time=market_date_time)
            sent_ding_msg(data)
        print(msg)
    else:
        msg = f'{company_name}({code}), 当前价格{today_price} 涨幅未超过 2%，涨幅: {k}%'
        print(msg)
        # sent_ding_msg(msg)


# 获取当前时间戳
current_timestamp = int(time_module.time() * 1000)


def is_beijing_market_open():
    beijing_time = datetime.utcnow() + timedelta(hours=8)
    market_open_morning = time(9, 20) <= beijing_time.time() <= time(12, 0)
    market_open_afternoon = time(13, 0) <= beijing_time.time() <= time(15, 0)
    return market_open_morning or market_open_afternoon


def job():
    if is_beijing_market_open():
        for code in array_stocks:
            compare_stock_code(code)
        print('~~~任务执行结束~~~')
    else:
        print('当前不是交易时间，任务未执行。')


# 创建一个调度器，并启动
scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', minutes=2)
scheduler.start()

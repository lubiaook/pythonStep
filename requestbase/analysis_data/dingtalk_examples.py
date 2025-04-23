import time

import dingtalk
import requests
import json

appkey = 'ding6at3fmyyvny2rldg'
appsecret = 'c4_uzBWoS6CVfSIjU2775k3XOE2WmjD7YT4S0pRJlpC6bm5YLj4EllhAAvbrzXfx'
url = 'https://oapi.dingtalk.com/gettoken?appkey=' + appkey + '&appsecret=' + appsecret
print(url)
response = requests.get(url)
response.raise_for_status()  # 检查请求是否成功
# 提取 JSON 数据
data_str = response.text
data = json.loads(data_str)

print(data['access_token'])
token = data['access_token']

post_sent_msg_url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=' + token
print(post_sent_msg_url)


# request_body={
#     "agent_id":3123423208,
# 	"msg":{
# 		"msgtype":"text",
# 		"text":{
# 			"content":"请填写周报5,小可爱们"
# 		}
# 	},
# 	"userid_list":"06490107591216996"
# }

def build_msg(rate, code, name, current_price, base_price, date):
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
                "text": f"#    \n   ### ({code}) {title}   \n * 当前价格：***{current_price}***    \n  * 成本价格: ***{base_price}***    \n * 日期： {date}  \n"

            }
        }
    }
    return data


request_body = {
    "agent_id": 3123423208,
    "userid_list": "06490107591216996",
    "msg": {
        "msgtype": "markdown",
        "markdown": {
            "title": "👏🏻 600180跌5%",
            "text": "# 💣 🧧一级标题   \n   ##     \n    * 列表1   \n   * 列表2  \n   * 列表3  \n  ![alt 啊](https://img.alicdn.com/tps/TB1XLjqNVXXXXc4XVXXXXXXXXXX-170-64.png) \n"

        }
    }
}

# 获取当前时间戳
current_timestamp = int(time.time() * 1000)

request_body = build_msg(-3, 600180, '瑞茂通', 5.5, 4.8, current_timestamp)
post_data = requests.post(url=post_sent_msg_url, json=request_body)

post_data.raise_for_status()  # 检查请求是否成功

print(post_data.text)

import asyncio
import requests


async def request(url):
    print('正在请求', url)
    print('请求成功', url)
    return url
    # async 修饰的函数，调用之后返回的一个协程对象
c = request('www.baidu.com')

# # 创建一个事件循环对象
# loop = asyncio.get_event_loop()
# # 将协程对象注册到loop中
# loop.run_until_complete(c)

loop = asyncio.get_event_loop()

# task的使用
# task = loop.create_task(c, name='new task')
# print(task)
# <Task pending name='Task-1' coro=<request() running at /Users/lubiaol/workspace/outfile/pythonLearn/requestbase/高性能异步爬虫/4.协程.py:5>>
# loop.run_until_complete(task)
# print(task)
# <Task finished name='Task-1' coro=<request() done, defined at /Users/lubiaol/workspace/outfile/pythonLearn/requestbase/高性能异步爬虫/4.协程.py:5> result=None>

# future 使用
# task2 = asyncio.ensure_future(c)
# print('执行前', task2)
# loop.run_until_complete(task2)
# print('执行后', task2)


def call_back_fuc(task3):
    # result 返回任务对象中封装的协程对象应用的函数返回值
    print(task3.result())


# 绑定回调
task3 = asyncio.ensure_future(c)
# 将回调函数绑定到任务对象中
task3.add_done_callback(call_back_fuc)
loop.run_until_complete(task3)

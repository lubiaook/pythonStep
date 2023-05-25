import requests
import asyncio
import time


async def request_def(url):
    print("开始调用", url)
    # request.get 是基于同步，必须使用基于异步的模块 aiohttp
    response = requests.get(url)
    print('调用完毕：', url, response.text)


start_time =time.time()
tasks = []
urls = {
    'http://127.0.0.1:5000/bobo',
    'http://127.0.0.1:5000/jay',
    'http://127.0.0.1:5000/lubiao',
}

loop = asyncio.get_event_loop()
for url in urls:
    c = request_def(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))

print(time.time()-start_time)
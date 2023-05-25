import asyncio
import requests
import asyncio
import time
import aiohttp


async def request_def(url):
    print("开始调用", url)
    # request.get 是基于同步，必须使用基于异步的模块 aiohttp
    # response = requests.get(url)
    async with aiohttp.ClientSession() as session:
        ## get()、post()
        ### headers,parmas/data.proxy =http://ip:port
        async with await session.get(url) as response:
            # text() 返回字符串形式的响应数据
            # read() 返回的二进制形式的响应数据
            #  json() 返回的是json对象
            # 注意 获取响应数据操作之前一定要使用 await 进行手动挂起
            page_text = await response.text()
            print('调用完毕：', url, response.text)


start_time = time.time()
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

print(time.time() - start_time)

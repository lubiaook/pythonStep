import asyncio
import time

asyncio


async def request(url):
    print('正在下载', url)
    # 如果在异步协程中如果出现了同步模块相关代码，那么就无法实现异步
    # time.sleep(2)
    # 当asyncio 中遇到阻塞操作必须手动进行挂起
    await asyncio.sleep(2)
    print('下载完毕', url)


startTime = time.time()
urls = {
    'www.baidu.com',
    'www.biling.com',
    'www.google.com'
}
loop = asyncio.get_event_loop()
tasks = []
for url in urls:
    c = request(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)
## 需要将任务列表封装到wait中
loop.run_until_complete(asyncio.wait(tasks))
print(time.time() - startTime)

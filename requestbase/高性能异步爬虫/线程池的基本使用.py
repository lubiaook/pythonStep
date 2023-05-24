import time
# 导入线程池
from multiprocessing.dummy import Pool

urlList = ['xiaozi', 'aa', 'bb', 'cc','ll','kk','gg']


startTime = time.time()
def getPage(str):
    print(str, "正在下载...")
    time.sleep(2)
    print(str, '下载完毕！')



# for url in urlList:
#     getPage(url)



# 实例化一个线城市对象
pool = Pool(4)
# 将列表中的每一个列表元素传递给get_page进行处理
pool.map(getPage, urlList)
endTime = time.time()
print('%d second' % (endTime - startTime))

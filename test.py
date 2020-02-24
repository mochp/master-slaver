# from yolo3.yolo import YOLO
import time
import os
from multiprocessing import Pool
from conf import config
import requests


def infer(port):
    url = "http://localhost:8889/master?modelId="+str(port)
    res = requests.get(url)
    return res.text


start = time.time()
p = Pool(64)   # 创建4个进程
for i in range(1000):
    p.apply_async(infer, args=(600,))
print('Waiting for all subprocesses done...')
p.close()
p.join()

print(time.time()-start)

# start = time.time()
# p = Pool(64)   # 创建4个进程
# for i in range(500):
#     p.apply_async(infer, args=(600,))
# print('Waiting for all subprocesses done...')
# p.close()
# p.join()

# print(time.time()-start)
# import threading
# import time
# import os
#
# def listen_music(num):
#     os.system(r'ffmpeg -f dshow -i video="@device_pnp_\\?\usb#vid_5986&pid_2115&mi_00#6&12786b7d&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global":audio="@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{0F432F25-11C9-4878-B21A-CCB5A879BED2}" -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -f flv rtmp://127.0.0.1:1935/live/test')
#
#
#
# if __name__ == '__main__':
#     t1 = threading.Thread(target=listen_music, args=(13,))
#
#     t1.start()
#
#
#
#
#
# import threading
# import time
#
# class myThread (threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print ("开启线程： " + self.name)
#         # 获取锁，用于线程同步
#         threadLock.acquire()
#         print_time(self.name, self.counter, 3)
#         # 释放锁，开启下一个线程
#         threadLock.release()
#
# def print_time(threadName, delay, counter):
#     while counter:
#         time.sleep(delay)
#         print ("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1
#
# threadLock = threading.Lock()
# threads = []
#
# # 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
#
# # 开启新线程
# thread1.start()
# thread2.start()
#
# # 添加线程到线程列表
# threads.append(thread1)
# threads.append(thread2)
#
# # 等待所有线程完成
# for t in threads:
#     t.join()
# print ("退出主线程")


import requests
import json

def infoReq(res):
    print(res.text)

def sendNotify(title, content):
    api = "https://sc.ftqq.com/xxxxxxxxxxxxxxxxxxxxxxxx.send"
    data = {
        "text":title,
        "desp":content
    }

    res = requests.post(api,data = data)
    infoReq(res)

if __name__ == '__main__':
    title = input("Input title:")
    content = input("Input content:")
    sendNotify(title, content)



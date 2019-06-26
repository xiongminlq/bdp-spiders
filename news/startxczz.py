# encoding: utf-8

"""
@author: 王良
@license: Apache Licence
@contact: 744516468@qq.com
@file: startxczz.py
@time: 2019/5/6 10:02
"""

import time
import schedule
import os


def start_spider():
    try:
        os.system("scrapy crawl xchzfzz")
        os.system("scrapy crawl bjzf")
        os.system("scrapy crawl chinapeace")
        now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        print('---{}---执行完成'.format(now_time))
        # 一定要先加载配置文件
    except Exception as e:
        print('--出现错误--', e)


if __name__ == '__main__':
    print('开始检测，等待时间到达，开始执行')
    # schedule.every().day.at("08:00").do(start_spider)
    start_spider()

    while True:
        schedule.run_pending()
        time.sleep(10)

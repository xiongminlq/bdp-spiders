# encoding: utf-8

"""
@author: 王良
@license: Apache Licence
@contact: 744516468@qq.com
@file: xiciproxy.py
@time: 2018/12/27 9:13
"""

import requests
import re
import time
import random
import telnetlib

keys = [
    'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
    'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3'
]

# 伪装浏览器
headers = {
    'User-Agent': keys[random.randint(0, len(keys) - 1)]
}


# 批量获取高匿代理ip
def getXCProxyIp(max_page_number):
    for i in range(1, max_page_number + 1):
        page_number = i
        init_url = 'http://www.xicidaili.com/nn/' + str(i)
        req = requests.get(init_url, headers=headers)
        # 获取代理ip
        agency_ip_re = re.compile(
            r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', re.S)
        agency_ip = agency_ip_re.findall(req.text)
        # 获取代理ip的端口号
        agency_port_re = re.compile('<td>([0-9]{2,5})</td>', re.S)
        agency_port = agency_port_re.findall(req.text)
        # 高匿代理ip页面中所列出的ip数量
        ip_number = len(agency_ip)
        print('正在获取第 %d 页代理中（请耐心等候）......' % page_number)
        for i in range(ip_number):
            total_ip = agency_ip[i] + ':' + agency_port[i]
            print(total_ip)
            verifyProxyIP(agency_ip[i], agency_port[i])
            time.sleep(1)
        print('第 %d 页代理获取完毕！' % page_number)
        print('------------------------------------')
        time.sleep(2)


# 验证获取到的代理IP是否可用
def verifyProxyIP(verify_ip, verify_ip_port):
    print('正在验证此代理IP是否可用......')
    try:
        proxies = {
            'http':'http://'+verify_ip+ ':' + verify_ip_port,
            'https': 'https://' + verify_ip + ':' + verify_ip_port
        }
        response = requests.get('https://www.qichacha.com', proxies=proxies)
        # telnetlib.Telnet(verify_ip, verify_ip_port, timeout=10)
    except:
        print('此代理IP不可用')
        print('-------------------------')
    else:
        print('此代理IP可用')
        print('-------------------------')
        available_ip = verify_ip + ':' + verify_ip_port
        saveProxyIP(available_ip)


# 将可用的代理IP保存到本地
def saveProxyIP(available_ip):
    with open('XCProxy.txt', 'a') as f:
        f.write(available_ip + '\n')


if __name__ == '__main__':
    print('---------- 高匿代理ip获取 ----------')
    getXCProxyIp(10)
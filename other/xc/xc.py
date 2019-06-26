# encoding: utf-8

"""
@author: 王良
@license: Apache Licence
@contact: 744516468@qq.com
@file: xc.py
@time: 2019/5/9 17:08
"""

import requests

url = 'http://search.people.com.cn/cnpeople/search.do'
data = {'siteName': 'news', 'pageNum': 1, 'keyword': '东坝', 'facetFlag': '', 'nodeType': 'belongsId',
        'nodeId': '0', 'pageCode': '', 'originName': ''}
headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Cookie': 'JSESSIONID=E4FFCBDDB8B0ABCBB096E64ACC47DB59; sfr=1; wdcid=58709ff400c89b34; ALLYESID4=10DA373BA4588097; sso_c=0; _people_ip_new_code=610000; _ma_tk=hk26i1qz1gpxue7y483yg50a4mniw8qx',
        'Origin': 'http://search.people.com.cn',
        'Upgrade-Insecure-Requests': '1'
    }
response = requests.post(url, data, headers=headers)
print(response.content)
url = 'http://search.people.com.cn/cnpeople/news/getNewsResult.jsp'
headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Cookie': 'JSESSIONID=E4FFCBDDB8B0ABCBB096E64ACC47DB59; sfr=1; wdcid=58709ff400c89b34; ALLYESID4=10DA373BA4588097; sso_c=0; _people_ip_new_code=610000; _ma_tk=hk26i1qz1gpxue7y483yg50a4mniw8qx',
        'Upgrade-Insecure-Requests': '1'
    }
print(requests.get(url, headers=headers))
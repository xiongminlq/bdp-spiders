# encoding: utf-8

"""
@author: ����
@license: Apache Licence
@contact: 744516468@qq.com
@file: xc.py
@time: 2019/5/9 17:08
"""

import json
import requests
import csv


def getColumn():
    columnss = {}
    #系统列表展示字段信息的url
    url = 'http://172.28.3.157:8080/xchzz/cenrep/queryByIdGridPanel.action?id=1015'
    result = json.loads(requests.post(url).content.decode())
    columnModel = result['columnModel'].replace('\n', '')
    columnModel = columnModel.split('{')
    for c in columnModel:
        c = c.replace('}', '')
        values = c.split(',')
        name = ''
        header = ''
        for value in values:
            value = value.split(':')
            if len(value) == 2:
                key = value[0].strip()
                value = value[1].replace('\'', '').strip()
                if key == 'name':
                    name = value
                elif key == 'header':
                    header = value
        if name != '' and header != '':
            columnss[name] = header
    print(columnss)
    return columnss

#解析字典url
def getDict(url):
    dict = {}
    result = json.loads(requests.post(url).content.decode())
    result = result['root']
    for r in result:
        dict[r['code']] = r['remark']
    return dict

def getData():
    columns = getColumn()
    values = list(columns.values())
    #保存地址及名称
    with open('data\\事件信息表.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values)
        writer.writeheader()
        start = 0
        limit = 1000
        #列表详情字段信息的url,包含了列表展示数据的总数
        url = 'http://172.28.3.157:8080/xchzz/community/event/queryByCondFormEventRegister.action'
        #获取Headers中Form Data的内容
        data = {'start': start, 'limit': limit,  'involvedperson': '',  'isExact': 0}
        result = json.loads(requests.post(url, data).content.decode())
        count = result['totalProperty']
        infos = result['root']
        if len(infos) > 0:
            #事件类型
            eventtype = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=MS_DIC_EVENTTYPE&_dc=1560433076824')
            #事件类别
            eventcategory = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=MS_DIC_EVENTCATEGORY&_dc=1560433076827')
            #事件来源
            infosource = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=MS_DIC_INFOSOURCE&_dc=1560433076827')

            for info in infos:
                row = {}
                for item in info:
                    if item in columns:
                        if item == 'eventtype' and info[item] in eventtype:
                            info[item] = eventtype[info[item]]
                        if item == 'eventcategory' and info[item] in eventcategory:
                            info[item] = eventcategory[info[item]]
                        if item == 'infosource' and info[item] in infosource:
                            info[item] = infosource[info[item]]

                        row[columns[item]] = info[item]
                writer.writerow(row)
            pageCount = (count - 1) // limit + 1
            if pageCount > 1:
                for i in range(1, pageCount + 1):
                    start = i * limit
                    data = {'start': start, 'limit': limit, 'involvedperson': '', 'isExact': 0}
                    result = json.loads(requests.post(url, data).content.decode())
                    infos = result['root']
                    if len(infos) > 0:
                        for info in infos:
                            row = {}
                            for item in info:
                                if item in columns:
                                    if item == 'eventtype' and info[item] in eventtype:
                                        info[item] = eventtype[info[item]]
                                    if item == 'eventcategory' and info[item] in eventcategory:
                                        info[item] = eventcategory[info[item]]
                                    if item == 'infosource' and info[item] in infosource:
                                        info[item] = infosource[info[item]]
                                    row[columns[item]] = info[item]
                            writer.writerow(row)
           
getData()






    

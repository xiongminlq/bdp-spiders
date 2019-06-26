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
    url = 'http://172.28.3.157:8080/xchzz/cenrep/queryByIdGridPanel.action?id=22'
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
    with open('data\\刑满释放_数据中心.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values)
        writer.writeheader()
        start = 0
        limit = 1000
        #列表详情字段信息的url,包含了列表展示数据的总数
        url = 'http://172.28.3.157:8080/xchzz/gx/GX_WT_CulpritManage/queryByCondFormWTCulpritManage.action'
        #获取Headers中Form Data的内容
        data = {'start': start, 'limit': limit, 'streetNo': '', 'streetCommNo': '',  'personName': '',  'idCard': '',  'isExact': 0}
        result = json.loads(requests.post(url, data).content.decode())
        count = result['totalProperty']
        infos = result['root']
        if len(infos) > 0:
            #街道编号
            streetNo = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETNO&_dc=1560479355857')
            #社区编号
            commNo = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_COMMNO&_dc=1560479355859')
            #性别
            sex = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_SEX&_dc=1560479356719')
            #是否重点管理
            isStressManage = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_ISMLPOBJECT&_dc=1560480281641')
            #当前状况
            nowStatus = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_NOWSTATUS&_dc=1560480281644')
            #表现情况
            acquitCircs = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_ACQUITCIRCS&_dc=1560480281646')
            #活动地区类型
            areaType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_AREATYPE&_dc=1560479366771')

            for info in infos:
                row = {}
                for item in info:
                    if item in columns:
                        if item == 'streetNo' and info[item] in streetNo:
                            info[item] = streetNo[info[item]]
                        if item == 'commNo' and info[item] in commNo:
                            info[item] = commNo[info[item]]
                        if item == 'sex' and info[item] in sex:
                            info[item] = sex[info[item]]
                        if item == 'isStressManage' and info[item] in isStressManage:
                            info[item] = isStressManage[info[item]]
                        if item == 'nowStatus' and info[item] in nowStatus:
                            info[item] = nowStatus[info[item]]
                        if item == 'acquitCircs' and info[item] in acquitCircs:
                            info[item] = acquitCircs[info[item]]
                        if item == 'areaType' and info[item] in areaType:
                            info[item] = areaType[info[item]]
                        row[columns[item]] = info[item]
                writer.writerow(row)
            pageCount = (count - 1) // limit + 1
            if pageCount > 1:
                for i in range(1, pageCount + 1):
                    start = i * limit
                    data = {'start': start, 'limit': limit, 'streetNo': '', 'streetCommNo': '', 'personName': '',
                            'idCard': '', 'isExact': 0}
                    result = json.loads(requests.post(url, data).content.decode())
                    infos = result['root']
                    if len(infos) > 0:
                        for info in infos:
                            row = {}
                            for item in info:
                                if item in columns:
                                    if item == 'streetNo' and info[item] in streetNo:
                                        info[item] = streetNo[info[item]]
                                    if item == 'commNo' and info[item] in commNo:
                                        info[item] = commNo[info[item]]
                                    if item == 'sex' and info[item] in sex:
                                        info[item] = sex[info[item]]
                                    if item == 'isStressManage' and info[item] in isStressManage:
                                        info[item] = isStressManage[info[item]]
                                    if item == 'nowStatus' and info[item] in nowStatus:
                                        info[item] = nowStatus[info[item]]
                                    if item == 'acquitCircs' and info[item] in acquitCircs:
                                        info[item] = acquitCircs[info[item]]
                                    if item == 'areaType' and info[item] in areaType:
                                        info[item] = areaType[info[item]]
                                    row[columns[item]] = info[item]
                            writer.writerow(row)
           
getData()






    

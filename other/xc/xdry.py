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
    url = 'http://172.28.3.157:8080/xchzz/cenrep/queryByIdGridPanel.action?id=579'
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
    with open('data\\吸毒人员.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values)
        writer.writeheader()
        start = 0
        limit = 1000
        #列表详情字段信息的url,包含了列表展示数据的总数
        url = 'http://172.28.3.157:8080/xchzz/peo/queryByCondFormDrugPerson.action'
        #获取Headers中Form Data的内容
        data = {'start': start, 'limit': limit, 'streetCode': '', 'religionType': '',  'commCode': '',  'marriAgeType': '',  'isExact': 0}
        result = json.loads(requests.post(url, data).content.decode())
        count = result['totalProperty']
        infos = result['root']
        if len(infos) > 0:
            #街道编码
            streetCode = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETNO&_dc=1560437546556')
            #社区编码
            commCode = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETCOMMNO&_dc=1560437683723')
            #性别
            sex = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_SEX&_dc=1560472078970')
            #婚姻状况
            marriAgeType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_MARRIAGETYPE&_dc=1560472078933')
            #籍贯
            nativePlace = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_AREACODE&_dc=1560472078968')
            #文化程度
            eduLevel = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_EDULEVEL&_dc=1560472078975')
            #民族
            nationAlity = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_FOLK&_dc=1560472078971')
            #政治面貌
            polity = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_POLITY&_dc=1560472078973')

            for info in infos:
                row = {}
                for item in info:
                    if item in columns:
                        if item == 'streetCode' and info[item] in streetCode:
                            info[item] = streetCode[info[item]]
                        if item == 'commCode' and info[item] in commCode:
                            info[item] = commCode[info[item]]
                        if item == 'sex' and info[item] in sex:
                            info[item] = sex[info[item]]
                        if item == 'nationAlity' and info[item] in nationAlity:
                            info[item] = nationAlity[info[item]]
                        if item == 'nativePlace' and info[item] in nativePlace:
                            info[item] = nativePlace[info[item]]
                        if item == 'marriAgeType' and info[item] in marriAgeType:
                            info[item] = marriAgeType[info[item]]
                        if item == 'polity' and info[item] in polity:
                            info[item] = polity[info[item]]
                        if item == 'eduLevel' and info[item] in eduLevel:
                            info[item] = eduLevel[info[item]]

                        row[columns[item]] = info[item]
                writer.writerow(row)
            pageCount = (count - 1) // limit + 1
            if pageCount > 1:
                for i in range(1, pageCount + 1):
                    start = i * limit
                    data = {'start': start, 'limit': limit, 'streetCode': '', 'religionType': '', 'commCode': '',
                            'marriAgeType': '', 'isExact': 0}
                    result = json.loads(requests.post(url, data).content.decode())
                    infos = result['root']
                    if len(infos) > 0:
                        for info in infos:
                            row = {}
                            for item in info:
                                if item in columns:
                                    if item == 'streetCode' and info[item] in streetCode:
                                        info[item] = streetCode[info[item]]
                                    if item == 'commCode' and info[item] in commCode:
                                        info[item] = commCode[info[item]]
                                    if item == 'sex' and info[item] in sex:
                                        info[item] = sex[info[item]]
                                    if item == 'nationAlity' and info[item] in nationAlity:
                                        info[item] = nationAlity[info[item]]
                                    if item == 'nativePlace' and info[item] in nativePlace:
                                        info[item] = nativePlace[info[item]]
                                    if item == 'marriAgeType' and info[item] in marriAgeType:
                                        info[item] = marriAgeType[info[item]]
                                    if item == 'polity' and info[item] in polity:
                                        info[item] = polity[info[item]]
                                    if item == 'eduLevel' and info[item] in eduLevel:
                                        info[item] = eduLevel[info[item]]
                                    row[columns[item]] = info[item]
                            writer.writerow(row)
           
getData()






    

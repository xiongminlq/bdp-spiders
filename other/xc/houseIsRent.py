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
    url = 'http://172.28.3.157:8080/xchzz/cenrep/queryByIdGridPanel.action?id=1002'
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
    #下载数据保存地址及文件名
    with open('data\\出租房屋信息表.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values)
        writer.writeheader()
        start = 0
        limit = 1000
        #列表详情字段信息的url,包含了列表展示数据的总数
        url = 'http://172.28.3.157:8080/xchzz/gather/flow/FP_FloatingRentHouse/queryByCondFormFloatingRentHouse.action'
        #获取Headers中Form Data的内容
        data = {'start': start, 'limit': limit, 'streetCode': '', 'isExact': 0,  'cenclLedgerId': 39}
        result = json.loads(requests.post(url, data).content.decode())
        count = result['totalProperty']
        infos = result['root']
        if len(infos) > 0:
            #所属街道
            streetCode = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_STREETCODE&_dc=1560426426973')
            #所属社区
            commCode = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_COMMCODE&_dc=1560426426975')
            #所有权类型
            ownerType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_OWNERTYPE&_dc=1560430494441')
            #性别
            sex = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_SEX&_dc=1560426426995')
            #证件类型
            cardType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_CARDTYPE&_dc=1560430494444')
            #政治面貌
            polity = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_POLITY&_dc=1560426427001')
            #户籍类别
            rprType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_RENTRPRTYPE&_dc=1560430494445')
            #建筑类型
            buildingType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_BUILDINGTYPE&_dc=1560430494451')
            #建设性质
            buildingProperty = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_BUILDINGPROPERTY&_dc=1560430494453')
            #所属派出所名称
            stationName = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_STATIONNAME&_dc=1560426427017')
            #民警姓名
            policeName = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_POLICENAME&_dc=1560426427019')
            #出租方式
            rentway = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_RENTWAY&_dc=1560430494454')
            #出租用途
            rentUse = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_RENTUSE&_dc=1560430494457')
            #出租类别
            rentType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_RENTTYPE&_dc=1560430494458')
            #租金年或月
            rentPeriod = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_RENTPERIOD&_dc=1560430494461')
            #证件类型
            subletCardType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_CARDTYPE&_dc=1560430494444')


            for info in infos:
                row = {}
                for item in info:
                    if item in columns:
                        if item == 'streetCode' and info[item] in streetCode:
                            info[item] = streetCode[info[item]]
                        if item == 'commCode' and info[item] in commCode:
                            info[item] = commCode[info[item]]
                        if item == 'ownerType' and info[item] in ownerType:
                            info[item] = ownerType[info[item]]
                        if item == 'sex' and info[item] in sex:
                            info[item] = sex[info[item]]
                        if item == 'cardType' and info[item] in cardType:
                            info[item] = cardType[info[item]]
                        if item == 'polity' and info[item] in polity:
                            info[item] = polity[info[item]]
                        if item == 'rprType' and info[item] in rprType:
                            info[item] = rprType[info[item]]
                        if item == 'buildingType' and info[item] in buildingType:
                            info[item] = buildingType[info[item]]
                        if item == 'buildingProperty' and info[item] in buildingProperty:
                            info[item] = buildingProperty[info[item]]
                        if item == 'policeName' and info[item] in policeName:
                            info[item] = policeName[info[item]]
                        if item == 'rentway' and info[item] in rentway:
                            info[item] = rentway[info[item]]
                        if item == 'rentUse' and info[item] in rentUse:
                            info[item] = rentUse[info[item]]
                        if item == 'rentType' and info[item] in rentType:
                            info[item] = rentType[info[item]]
                        if item == 'rentPeriod' and info[item] in rentPeriod:
                            info[item] = rentPeriod[info[item]]
                        if item == 'subletCardType' and info[item] in subletCardType:
                            info[item] = subletCardType[info[item]]

                        row[columns[item]] = info[item]
                writer.writerow(row)
            pageCount = (count - 1) // limit + 1
            if pageCount > 1:
                for i in range(1, pageCount + 1):
                    start = i * limit
                    data = {'start': start, 'limit': limit, 'streetCode': '', 'isExact': 0, 'cenclLedgerId': 39}
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
                                    if item == 'ownerType' and info[item] in ownerType:
                                        info[item] = ownerType[info[item]]
                                    if item == 'sex' and info[item] in sex:
                                        info[item] = sex[info[item]]
                                    if item == 'cardType' and info[item] in cardType:
                                        info[item] = cardType[info[item]]
                                    if item == 'polity' and info[item] in polity:
                                        info[item] = polity[info[item]]
                                    if item == 'rprType' and info[item] in rprType:
                                        info[item] = rprType[info[item]]
                                    if item == 'buildingType' and info[item] in buildingType:
                                        info[item] = buildingType[info[item]]
                                    if item == 'buildingProperty' and info[item] in buildingProperty:
                                        info[item] = buildingProperty[info[item]]
                                    if item == 'policeName' and info[item] in policeName:
                                        info[item] = policeName[info[item]]
                                    if item == 'rentway' and info[item] in rentway:
                                        info[item] = rentway[info[item]]
                                    if item == 'rentUse' and info[item] in rentUse:
                                        info[item] = rentUse[info[item]]
                                    if item == 'rentType' and info[item] in rentType:
                                        info[item] = rentType[info[item]]
                                    if item == 'rentPeriod' and info[item] in rentPeriod:
                                        info[item] = rentPeriod[info[item]]
                                    if item == 'subletCardType' and info[item] in subletCardType:
                                        info[item] = subletCardType[info[item]]
                                    row[columns[item]] = info[item]
                            writer.writerow(row)
           
getData()






    

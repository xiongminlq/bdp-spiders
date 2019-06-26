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
    url = 'http://172.28.3.157:8080/xchzz/cenrep/queryByIdGridPanel.action?id=928'
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
    with open('data\\楼栋表.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values)
        writer.writeheader()
        start = 0
        limit = 1000
        #列表详情字段信息的url,包含了列表展示数据的总数
        url = 'http://172.28.3.157:8080/xchzz/community/site/HA_Building/queryByCondFormBuilding.action'
        #获取Headers中Form Data的内容
        data = {'start': start, 'limit': limit, 'streetNo': '',  'roomType': '', 'commNo': '',  'buildingUse': '',    'buildingNo': '',    'buildingName': '',  'isExact': 0,  'cenclLedgerId': 7}
        result = json.loads(requests.post(url, data).content.decode())
        count = result['totalProperty']
        infos = result['root']
        if len(infos) > 0:
            #街道名称
            streetNo = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETNO&_dc=1560420764378')
            #社区名称
            commNo = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_COMMNO&_dc=1560420764380')
            #房屋类型
            roomType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=HA_DIC_ROOMTYPE&_dc=1560426546090')
            #建筑物用途
            buildingUse = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=HA_DIC_BUILDINGUSE&_dc=1560426546094')
            #建筑结构
            buildingStruture = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=HA_DIC_BUILDINGSTRUTURE&_dc=1560426546117')
            #是否有公厕
            isToilet = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=HA_DIC_ISSAVE&_dc=1560426546119')
            #水表是否分户
            isWaterDispart = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=HA_DIC_ISSAVE&_dc=1560426546119')
            #电表是否分户
            isAmmeterDispart = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=HA_DIC_ISSAVE&_dc=1560426546119')
            #是否临时保存
            isSave = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=HA_DIC_ISSAVE&_dc=1560426546119')

            for info in infos:
                row = {}
                for item in info:
                    if item in columns:
                        if item == 'streetNo' and info[item] in streetNo:
                            info[item] = streetNo[info[item]]
                        if item == 'commNo' and info[item] in commNo:
                            info[item] = commNo[info[item]]
                        if item == 'roomType' and info[item] in roomType:
                            info[item] = roomType[info[item]]
                        if item == 'buildingUse' and info[item] in buildingUse:
                            info[item] = buildingUse[info[item]]
                        if item == 'buildingStruture' and info[item] in buildingStruture:
                            info[item] = buildingStruture[info[item]]
                        if item == 'isToilet' and info[item] in isToilet:
                            info[item] = isToilet[info[item]]
                        if item == 'isWaterDispart' and info[item] in isWaterDispart:
                            info[item] = isWaterDispart[info[item]]
                        if item == 'isAmmeterDispart' and info[item] in isAmmeterDispart:
                            info[item] = isAmmeterDispart[info[item]]
                        if item == 'isSave' and info[item] in isSave:
                            info[item] = isSave[info[item]]

                        row[columns[item]] = info[item]
                writer.writerow(row)
            pageCount = (count - 1) // limit + 1
            if pageCount > 1:
                for i in range(1, pageCount + 1):
                    start = i * limit
                    # 获取Headers中Form Data的内容
                    data = {'start': start, 'limit': limit, 'streetNo': '', 'roomType': '', 'commNo': '',
                            'buildingUse': '', 'buildingNo': '', 'buildingName': '', 'isExact': 0, 'cenclLedgerId': 7}
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
                                    if item == 'roomType' and info[item] in roomType:
                                        info[item] = roomType[info[item]]
                                    if item == 'buildingUse' and info[item] in buildingUse:
                                        info[item] = buildingUse[info[item]]
                                    if item == 'buildingStruture' and info[item] in buildingStruture:
                                        info[item] = buildingStruture[info[item]]
                                    if item == 'isToilet' and info[item] in isToilet:
                                        info[item] = isToilet[info[item]]
                                    if item == 'isWaterDispart' and info[item] in isWaterDispart:
                                        info[item] = isWaterDispart[info[item]]
                                    if item == 'isAmmeterDispart' and info[item] in isAmmeterDispart:
                                        info[item] = isAmmeterDispart[info[item]]
                                    if item == 'isSave' and info[item] in isSave:
                                        info[item] = isSave[info[item]]
                                    row[columns[item]] = info[item]
                            writer.writerow(row)
           
getData()






    

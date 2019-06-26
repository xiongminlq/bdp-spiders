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
    url = 'http://172.28.3.157:8080/xchzz/cenrep/queryByIdGridPanel.action?id=11'
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
    with open('data\\户籍人口表.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values)
        writer.writeheader()
        start = 0
        limit = 1000
        #列表详情字段信息的url,包含了列表展示数据的总数
        url = 'http://172.28.3.157:8080/xchzz/gx/GX_JC_Rpr/queryByCondFormRpr.action'
        #获取Headers中Form Data的内容
        data = {'start': start, 'limit': limit, 'streetNo': '', 'streetCommNo': '',  'hostName': '',  'hostName': '',  'isExact': 0}
        result = json.loads(requests.post(url, data).content.decode())
        count = result['totalProperty']
        infos = result['root']
        if len(infos) > 0:
            #性别
            sex = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_SEX&_dc=1560409345755')
            #所属街道
            street = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETNO&_dc=1560404352357')
            #所属社区
            community = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETCOMMNO&_dc=1560404353125')
            #是否救助
            #isSave = getDict('')
            #户籍状态
            rprStatus = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_RPRSTATUS&_dc=1560409345782')
            #家庭人均收入级别
            familyIncome = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_FAMILYINCOME&_dc=1560409359319')
            #户结构
            rprStructure = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_RPRSTRUCTURE&_dc=1560409359322')

            for info in infos:
                row = {}
                for item in info:
                    if item in columns:
                        if item == 'sex' and info[item] in sex:
                            info[item] = sex[info[item]]
                        if item == 'street' and info[item] in street:
                            info[item] = street[info[item]]
                        if item == 'community' and info[item] in community:
                            info[item] = community[info[item]]
                        if item == 'rprStatus' and info[item] in rprStatus:
                            info[item] = rprStatus[info[item]]
                        if item == 'familyIncome' and info[item] in familyIncome:
                            info[item] = familyIncome[info[item]]
                        if item == 'rprStructure' and info[item] in rprStructure:
                            info[item] = rprStructure[info[item]]

                        row[columns[item]] = info[item]
                writer.writerow(row)
            pageCount = (count - 1) // limit + 1
            if pageCount > 1:
                for i in range(1, pageCount + 1):
                    start = i * limit
                    data = {'start': start, 'limit': limit, 'streetNo': '', 'streetCommNo': '', 'initStart': '', 'idCard': '', 'personName': '', 'isExact': 0, 'initEnd': '', 'dataSource' : '', 'cenclLedgerId': 9}
                    result = json.loads(requests.post(url, data).content.decode())
                    infos = result['root']
                    if len(infos) > 0:
                        for info in infos:
                            row = {}
                            for item in info:
                                if item in columns:
                                    if item == 'sex' and info[item] in sex:
                                        info[item] = sex[info[item]]
                                    if item == 'street' and info[item] in street:
                                        info[item] = street[info[item]]
                                    if item == 'community' and info[item] in community:
                                        info[item] = community[info[item]]
                                    if item == 'rprStatus' and info[item] in rprStatus:
                                        info[item] = rprStatus[info[item]]
                                    if item == 'familyIncome' and info[item] in familyIncome:
                                        info[item] = familyIncome[info[item]]
                                    if item == 'rprStructure' and info[item] in rprStructure:
                                        info[item] = rprStructure[info[item]]
                                    row[columns[item]] = info[item]
                            writer.writerow(row)
           
getData()






    

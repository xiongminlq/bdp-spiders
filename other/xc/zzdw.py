# encoding: utf-8

"""
@author: 王良
@license: Apache Licence
@contact: 744516468@qq.com
@file: xc.py
@time: 2019/5/9 17:08
"""

import json
import requests
import xlwt


def addCellValue(sheet, row, values):
    for i in range(len(values)):
        sheet.write(row, i, values[i])


def getColumn():
    columns = {}
    url = 'http://172.28.3.157:8080/xchzxt/cenrep/queryByIdGridPanel.action?id=1202'
    result = json.loads(requests.post(url).content.decode())
    columnModel = result['columnModel'].replace('[', '').replace(']', '').replace('\n', '')
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
            columns[name] = header
    return columns

def getDict(url):
    dict = {}
    result = json.loads(requests.post(url).content.decode())
    result = result['root']
    for r in result:
        dict[r['code']] = r['remark']
    return dict

def getData():
    newBook = xlwt.Workbook(encoding='utf-8')
    sheet = newBook.add_sheet('sheet1')
    columns = getColumn()
    values = list(columns.values())
    addCellValue(sheet, 0, values)
    start = 0
    limit = 1000
    url = 'http://172.28.3.157:8080/xchzxt/team/queryByCondFormRANKS.action'
    data = {'start': start, 'limit': limit, 'name': '', 'nation': '', 'politic': '', 'isExact': 0}
    result = json.loads(requests.post(url, data).content.decode())
    count = result['totalProperty']
    infos = result['root']
    index = 0
    print('count', count)
    if len(infos) > 0:
        nation = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_NATIONALITY&_dc=1557733325804')
        polity = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_POLITY&_dc=1557733325809')
        sex = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_SEX&_dc=1557733325843')
        edulevel = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_EDULEVEL&_dc=1557733325847')
        computerlevel = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=ZZ_DIC_COMPUTERLEVEL&_dc=1557733325849')
        englishlevel = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=ZZ_DIC_ENGLISHLEVEL&_dc=1557733325852')
        for info in infos:
            values = []
            for i in columns:
                value = info[i] if i in info else ''
                if i == 'nation' and value in nation:
                    value = nation[value]
                elif i == 'politic' and value in polity:
                    value = polity[value]
                elif i == 'sex' and value in sex:
                    value = sex[value]
                elif i == 'edu' and value in edulevel:
                    value = edulevel[value]
                elif i == 'it_level' and value in computerlevel:
                    value = computerlevel[value]
                elif i == 'language' and value in englishlevel:
                    value = englishlevel[value]
                values.append(value)
            index += 1
            addCellValue(sheet, index, values)
        pageCount = (count - 1) // limit + 1
        print('pageCount',pageCount)
        if pageCount > 1:
            for i in range(1, pageCount + 1):
                start = i * limit
                data = {'start': start, 'limit': limit, 'name': '', 'nation': '', 'politic': '', 'isExact': 0}
                result = json.loads(requests.post(url, data).content.decode())
                infos = result['root']
                if len(infos) > 0:
                    for info in infos:
                        values = []
                        for j in columns:
                            value = info[j] if j in info else ''
                            if j == 'nation' and value in nation:
                                value = nation[value]
                            elif j == 'politic' and value in polity:
                                value = polity[value]
                            elif j == 'sex' and value in sex:
                                value = sex[value]
                            elif j == 'edu' and value in edulevel:
                                value = edulevel[value]
                            elif j == 'it_level' and value in computerlevel:
                                value = computerlevel[value]
                            elif j == 'language' and value in englishlevel:
                                value = englishlevel[value]
                            values.append(value)
                        index += 1
                        addCellValue(sheet, index, values)
    newBook.save('data\综治队伍.xls')


getData()

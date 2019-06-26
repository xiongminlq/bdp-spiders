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
    url = 'http://172.28.3.157:8080/xchzxt/cenrep/queryByIdGridPanel.action?id=585'
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
    limit = 100
    url = 'http://172.28.3.157:8080/xchzxt/zzorg/queryByCondFormdisputes.action'
    data = {'start': start, 'limit': limit, 'streetCode': '', 'eventType': '', 'commCode': '', 'eventArea': '', 'isExact': 0}
    result = json.loads(requests.post(url, data).content.decode())
    count = result['totalProperty']
    infos = result['root']
    index = 0
    print('count', count)
    if len(infos) > 0:
        eventtype = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=ZZ_DIC_EVENTTYPE&_dc=1557756126676')
        eventarea = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=ZZ_DIC_EVENTAREA&_dc=1557756126684')
        lawidcardtype = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=ZZ_DIC_LAWIDCARDTYPE&_dc=1557756126728')
        mediateway = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=ZZ_DIC_MEDIATEWAY&_dc=1557756126730')
        streetcode = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETNO&_dc=1557756126669')
        commcode = getDict('http://172.28.3.157:8080/xchzxt/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETCOMMNO&_dc=1557756126680')
        for info in infos:
            values = []
            for i in columns:
                value = info[i] if i in info else ''
                if i == 'eventType' and value in eventtype:
                    value = eventtype[value]
                elif i == 'eventArea' and value in eventarea:
                    value = eventarea[value]
                elif i == 'privyIdCardType' and value in lawidcardtype:
                    value = lawidcardtype[value]
                elif i == 'mediateWay' and value in mediateway:
                    value = mediateway[value]
                elif i == 'streetCode' and value in streetcode:
                    value = streetcode[value]
                elif i == 'commCode' and value in commcode:
                    value = commcode[value]
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
                            if i == 'eventType' and value in eventtype:
                                value = eventtype[value]
                            elif i == 'eventArea' and value in eventarea:
                                value = eventarea[value]
                            elif i == 'privyIdCardType' and value in lawidcardtype:
                                value = lawidcardtype[value]
                            elif i == 'mediateWay' and value in mediateway:
                                value = mediateway[value]
                            elif i == 'streetCode' and value in streetcode:
                                value = streetcode[value]
                            elif i == 'commCode' and value in commcode:
                                value = commcode[value]
                            values.append(value)
                        index += 1
                        addCellValue(sheet, index, values)
    newBook.save('data\矛调事件管理.xls')


getData()

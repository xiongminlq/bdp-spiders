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
    url = 'http://172.28.3.157:8080/xchzz/cenrep/queryByIdGridPanel.action?id=24'
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
            columns[name] = header
    print(columns)
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
    url = 'http://172.28.3.157:8080/xchzz/gx/GX_SW_DeadInfo/queryByCondFormSWDeadInfo.action'
    data = {'start': start, 'limit': limit, 'streetNo': '', 'streetCommNo': '', 'personName': '', 'idCard': '', 'isExact': 0}
    result = json.loads(requests.post(url, data).content.decode())
    count = result['totalProperty']
    infos = result['root']
    index = 0
    print('count', count)
    if len(infos) > 0:
        sex = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_SEX&_dc=1560340930618')
        deathReason = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_DEATHREASON&_dc=1560341041933')
        street = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETNO&_dc=1560340929837')
        community = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=CL_DIC_COMMCODE&_dc=1560340929824')
        logoff  = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_ISMLPOBJECT&_dc=1560341041936')
        for info in infos:
            values = []
            for i in columns:
                value = info[i] if i in info else ''
                if i == 'sex' and value in sex:
                    value = sex[value]
                if i == 'deathReason' and value in deathReason:
                    value = deathReason[value]
                if i == 'street' and value in street:
                    value = street[value]
                if i == 'community' and value in community:
                    value = community[value]
                if i == 'logoff' and value in logoff:
                    value = logoff[value]
                values.append(value)
            index += 1
            addCellValue(sheet, index, values)
        pageCount = (count - 1) // limit + 1
        print('pageCount',pageCount)
        if pageCount > 1:
            for i in range(1, pageCount + 1):
                start = i * limit
                data = {'start': start, 'limit': limit, 'streetNo': '', 'streetCommNo': '', 'initStart': '', 'idCard': '', 'personName': '', 'isExact': 0, 'initEnd': '', 'dataSource' : '', 'cenclLedgerId': 9}
                result = json.loads(requests.post(url, data).content.decode())
                infos = result['root']
                if len(infos) > 0:
                    for info in infos:
                        values = []
                        for j in columns:
                            value = info[j] if j in info else ''
                            if i == 'sex' and value in sex:
                                value = sex[value]
                            if i == 'deathReason' and value in deathReason:
                                value = deathReason[value]
                            if i == 'street' and value in street:
                                value = street[value]
                            if i == 'community' and value in community:
                                value = community[value]
                            if i == 'logoff' and value in logoff:
                                value = logoff[value]
                            values.append(value)
                        index += 1
                        addCellValue(sheet, index, values)
    newBook.save('data\死亡人员信息表.xls')


getData()

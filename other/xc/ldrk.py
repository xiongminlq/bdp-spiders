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
    url = 'http://172.28.3.157:8080/xchzz/cenrep/queryByIdGridPanel.action?id=2'
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
    with open('data\\流动人口表.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values)
        writer.writeheader()
        start = 0
        limit = 1000
        #列表详情字段信息的url,包含了列表展示数据的总数
        url = 'http://172.28.3.157:8080/xchzz/gather/flow/FP_FloatingPopulation/queryByCondFormFloatingPopulation.action'
        #获取Headers中Form Data的内容
        data = {'start': start, 'limit': limit, 'streetCode': '', 'commCode': '',  'name': '',  'iDCard': '',  'isExact': 0}
        result = json.loads(requests.post(url, data).content.decode())
        count = result['totalProperty']
        infos = result['root']
        if len(infos) > 0:
            #性别
            sex = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_SEX&_dc=1560410230522')
            #所属街道
            street = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_STREETCODE&_dc=1560410230490')
            #所属社区
            community = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_COMMCODE&_dc=1560410230494')
            #民族
            nationality = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_NATIONALITY&_dc=1560410230527')
            #政治面貌
            polity = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_POLITY&_dc=1560410230528')
            #教育水平
            eduLevel = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_EDULEVEL&_dc=1560410230528')
            #户籍类别
            rprType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_POPRPRTYPE&_dc=1560410230531')
            #婚姻状态
            marrStatus = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_MARRSTATUS&_dc=1560410230535')
            #有无居住证件
            isLivingCard = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_ISLIVINGCARD&_dc=1560410230532')
            #婚育证明
            marrProof = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_MARRPROOF&_dc=1560410230537')
            #免疫接种
            isImmunize = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_ISIMMUNIZE&_dc=1560410230540')
            #家庭户流入
            isFamilyFlow = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_ISFAMILYFLOW&_dc=1560410230541')
            #来京原因
            comeReason = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_COMEREASON&_dc=1560410230544')
            #居住类型
            livingType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_LIVINGTYPE&_dc=1560410230544')
            #民警姓名
            policeName = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_POLICENAME&_dc=1560410230548')
            #目前状况
            nowStatus = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_NOWSTATUS&_dc=1560410230551')
            #就业单位行业
            industry = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_INDUSTRY&_dc=1560410230553')
            #职业
            occupation = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_OCCUPATION&_dc=1560410230556')
            #主要从事工作
            work = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_WORK&_dc=1560410230555')
            #管理员
            managerName = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_MANAGERNAME&_dc=1560410230524')
            #所属派出所名称
            stationName = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=FP_DIC_STATIONNAME&_dc=1560410230546')

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
                        if item == 'nationality' and info[item] in nationality:
                            info[item] = nationality[info[item]]
                        if item == 'polity' and info[item] in polity:
                            info[item] = polity[info[item]]
                        if item == 'eduLevel' and info[item] in eduLevel:
                            info[item] = eduLevel[info[item]]
                        if item == 'rprType' and info[item] in rprType:
                            info[item] = rprType[info[item]]
                        if item == 'marrStatus' and info[item] in marrStatus:
                            info[item] = marrStatus[info[item]]
                        if item == 'isLivingCard' and info[item] in isLivingCard:
                            info[item] = isLivingCard[info[item]]
                        if item == 'marrProof' and info[item] in marrProof:
                            info[item] = marrProof[info[item]]
                        if item == 'isImmunize' and info[item] in isImmunize:
                            info[item] = isImmunize[info[item]]
                        if item == 'isFamilyFlow' and info[item] in isFamilyFlow:
                            info[item] = isFamilyFlow[info[item]]
                        if item == 'comeReason' and info[item] in comeReason:
                            info[item] = comeReason[info[item]]
                        if item == 'livingType' and info[item] in livingType:
                            info[item] = livingType[info[item]]
                        if item == 'nowStatus' and info[item] in nowStatus:
                            info[item] = nowStatus[info[item]]
                        if item == 'industry' and info[item] in industry:
                            info[item] = industry[info[item]]
                        if item == 'policeName' and info[item] in policeName:
                            info[item] = policeName[info[item]]
                        if item == 'occupation' and info[item] in occupation:
                            info[item] = occupation[info[item]]
                        if item == 'work' and info[item] in work:
                            info[item] = work[info[item]]
                        if item == 'managerName' and info[item] in managerName:
                            info[item] = managerName[info[item]]
                        if item == 'stationName' and info[item] in stationName:
                            info[item] = stationName[info[item]]

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
                                    if item == 'nationality' and info[item] in nationality:
                                        info[item] = nationality[info[item]]
                                    if item == 'polity' and info[item] in polity:
                                        info[item] = polity[info[item]]
                                    if item == 'eduLevel' and info[item] in eduLevel:
                                        info[item] = eduLevel[info[item]]
                                    if item == 'rprType' and info[item] in rprType:
                                        info[item] = rprType[info[item]]
                                    if item == 'marrStatus' and info[item] in marrStatus:
                                        info[item] = marrStatus[info[item]]
                                    if item == 'isLivingCard' and info[item] in isLivingCard:
                                        info[item] = isLivingCard[info[item]]
                                    if item == 'marrProof' and info[item] in marrProof:
                                        info[item] = marrProof[info[item]]
                                    if item == 'isImmunize' and info[item] in isImmunize:
                                        info[item] = isImmunize[info[item]]
                                    if item == 'isFamilyFlow' and info[item] in isFamilyFlow:
                                        info[item] = isFamilyFlow[info[item]]
                                    if item == 'comeReason' and info[item] in comeReason:
                                        info[item] = comeReason[info[item]]
                                    if item == 'livingType' and info[item] in livingType:
                                        info[item] = livingType[info[item]]
                                    if item == 'nowStatus' and info[item] in nowStatus:
                                        info[item] = nowStatus[info[item]]
                                    if item == 'industry' and info[item] in industry:
                                        info[item] = industry[info[item]]
                                    if item == 'policeName' and info[item] in policeName:
                                        info[item] = policeName[info[item]]
                                    if item == 'occupation' and info[item] in occupation:
                                        info[item] = occupation[info[item]]
                                    if item == 'work' and info[item] in work:
                                        info[item] = work[info[item]]
                                    if item == 'managerName' and info[item] in managerName:
                                        info[item] = managerName[info[item]]
                                    if item == 'stationName' and info[item] in stationName:
                                        info[item] = stationName[info[item]]
                                    row[columns[item]] = info[item]
                            writer.writerow(row)
           
getData()






    

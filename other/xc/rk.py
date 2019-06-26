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
    url = 'http://172.28.3.157:8080/xchzz/cenrep/queryByIdGridPanel.action?id=930'
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
    with open('data\\人口基本信息表.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values)
        writer.writeheader()
        start = 0
        limit = 1000
        url = 'http://172.28.3.157:8080/xchzz/gx/GX_PersonInfo/queryByCondFormPersonInfo.action'
        data = {'start': start, 'limit': limit, 'streetNo': '', 'streetCommNo': '', 'initStart': '', 'idCard': '', 'personName': '', 'isExact': 0, 'initEnd': '', 'dataSource' : '', 'cenclLedgerId': 9}
        result = json.loads(requests.post(url, data).content.decode())
        count = result['totalProperty']
        infos = result['root']
        if len(infos) > 0:
            #性别
            sex = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_SEX&_dc=1560404353212')
            #所属街道
            street = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETNO&_dc=1560404352357')
            #所属社区
            community = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETCOMMNO&_dc=1560404353125')
            #与户主关系
            relation = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_FAMILYRELAT&_dc=1560404353205')
            #国家（地区）
            countRy = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_COUNTRY&_dc=1560404353208')
            #证件类别
            idCardType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_IDCARDTYPE&_dc=1560404353209')
            #民族
            nationAlity = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_FOLK&_dc=1560404353213')
            #籍贯
            nativePlace = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_AREACODE&_dc=1560404353215')
            #血型
            bloodType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_BLOODTYPE&_dc=1560404353219')
            #政治面貌
            polity = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_POLITY&_dc=1560404353221')
            #文化程度
            eduLevel = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_EDULEVEL&_dc=1560404353223')
            #是否社区直管党员
            isCommParty = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_ISCOMMPARTY&_dc=1560404353251')
            #健康状况
            healthType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_HEALTHTYPE&_dc=1560404353225')
            #婚姻状况
            marriAgeType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_MARRIAGETYPE&_dc=1560404353228')
            #已婚分类
            marrType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_MARRTYPE&_dc=1560404353230')
            #是否涉外婚姻
            isForeignMarriAge = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_ISCOMMPARTY&_dc=1560404353251')
            #兵役状况
            miliTaryType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_MILITARYTYPE&_dc=1560404353233')
            #宗教信仰
            religionType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_RELIGIONTYPE&_dc=1560404353234')
            #从业状况
            jobStatus = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_JOBSTATUS&_dc=1560404353238')
            #个人户籍状态
            rprStatus = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_RPRSTATUS&_dc=1560404353239')
            #特长
            suit = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_SUIT&_dc=1560404353244')
            #户口类别
            rprType = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_RPRTYPE&_dc=1560404353245')
            #未迁户口原因
            unMoveReason = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_NOOUTRPRREASON&_dc=1560404353249')
            #数据来源
            dataSource = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_DATASOURCE&_dc=1560404353128')
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
                        if item == 'relation' and info[item] in relation:
                            info[item] = relation[info[item]]
                        if item == 'countRy' and info[item] in countRy:
                            info[item] = countRy[info[item]]
                        if item == 'idCardType' and info[item] in idCardType:
                            info[item] = idCardType[info[item]]
                        if item == 'nationAlity' and info[item] in nationAlity:
                            info[item] = nationAlity[info[item]]
                        if item == 'nativePlace' and info[item] in nativePlace:
                            info[item] = nativePlace[info[item]]
                        if item == 'bloodType' and info[item] in bloodType:
                            info[item] = bloodType[info[item]]
                        if item == 'polity' and info[item] in polity:
                            info[item] = polity[info[item]]
                        if item == 'eduLevel' and info[item] in eduLevel:
                            info[item] = eduLevel[info[item]]
                        if item == 'isCommParty' and info[item] in isCommParty:
                            info[item] = isCommParty[info[item]]
                        if item == 'healthType' and info[item] in healthType:
                            info[item] = healthType[info[item]]
                        if item == 'marriAgeType' and info[item] in marriAgeType:
                            info[item] = marriAgeType[info[item]]
                        if item == 'marrType' and info[item] in marrType:
                            info[item] = marrType[info[item]]
                        if item == 'isForeignMarriAge' and info[item] in isForeignMarriAge:
                            info[item] = isForeignMarriAge[info[item]]
                        if item == 'miliTaryType' and info[item] in miliTaryType:
                            info[item] = miliTaryType[info[item]]
                        if item == 'religionType' and info[item] in religionType:
                            info[item] = religionType[info[item]]
                        if item == 'jobStatus' and info[item] in jobStatus:
                            info[item] = jobStatus[info[item]]
                        if item == 'rprStatus' and info[item] in rprStatus:
                            info[item] = rprStatus[info[item]]
                        if item == 'suit' and info[item] in suit:
                            info[item] = suit[info[item]]
                        if item == 'rprType' and info[item] in rprType:
                            info[item] = rprType[info[item]]
                        if item == 'unMoveReason' and info[item] in unMoveReason:
                            info[item] = unMoveReason[info[item]]
                        if item == 'dataSource' and info[item] in dataSource:
                            info[item] = dataSource[info[item]]

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
                                    if item == 'relation' and info[item] in relation:
                                        info[item] = relation[info[item]]
                                    if item == 'countRy' and info[item] in countRy:
                                        info[item] = countRy[info[item]]
                                    if item == 'idCardType' and info[item] in idCardType:
                                        info[item] = idCardType[info[item]]
                                    if item == 'nationAlity' and info[item] in nationAlity:
                                        info[item] = nationAlity[info[item]]
                                    if item == 'nativePlace' and info[item] in nativePlace:
                                        info[item] = nativePlace[info[item]]
                                    if item == 'bloodType' and info[item] in bloodType:
                                        info[item] = bloodType[info[item]]
                                    if item == 'polity' and info[item] in polity:
                                        info[item] = polity[info[item]]
                                    if item == 'eduLevel' and info[item] in eduLevel:
                                        info[item] = eduLevel[info[item]]
                                    if item == 'isCommParty' and info[item] in isCommParty:
                                        info[item] = isCommParty[info[item]]
                                    if item == 'healthType' and info[item] in healthType:
                                        info[item] = healthType[info[item]]
                                    if item == 'marriAgeType' and info[item] in marriAgeType:
                                        info[item] = marriAgeType[info[item]]
                                    if item == 'marrType' and info[item] in marrType:
                                        info[item] = marrType[info[item]]
                                    if item == 'isForeignMarriAge' and info[item] in isForeignMarriAge:
                                        info[item] = isForeignMarriAge[info[item]]
                                    if item == 'miliTaryType' and info[item] in miliTaryType:
                                        info[item] = miliTaryType[info[item]]
                                    if item == 'religionType' and info[item] in religionType:
                                        info[item] = religionType[info[item]]
                                    if item == 'jobStatus' and info[item] in jobStatus:
                                        info[item] = jobStatus[info[item]]
                                    if item == 'rprStatus' and info[item] in rprStatus:
                                        info[item] = rprStatus[info[item]]
                                    if item == 'suit' and info[item] in suit:
                                        info[item] = suit[info[item]]
                                    if item == 'rprType' and info[item] in rprType:
                                        info[item] = rprType[info[item]]
                                    if item == 'unMoveReason' and info[item] in unMoveReason:
                                        info[item] = unMoveReason[info[item]]
                                    if item == 'dataSource' and info[item] in dataSource:
                                        info[item] = dataSource[info[item]]
                                    row[columns[item]] = info[item]
                            writer.writerow(row)
           
getData()






    

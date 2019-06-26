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
    url = 'http://172.28.3.157:8080/xchzz/cenrep/queryByIdGridPanel.action?id=27'
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
    with open('data\\精神病人_数据中心.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values)
        writer.writeheader()
        start = 0
        limit = 1000
        #列表详情字段信息的url,包含了列表展示数据的总数
        url = 'http://172.28.3.157:8080/xchzz/gx/GX_JZ_LunacyPrevCure/queryByCondFormJZLunacyPrevCure.action'
        #获取Headers中Form Data的内容
        data = {'start': start, 'limit': limit, 'streetNo': '', 'streetCommNo': '',  'personName': '',  'idCard': '',  'isExact': 0}
        result = json.loads(requests.post(url, data).content.decode())
        count = result['totalProperty']
        infos = result['root']
        if len(infos) > 0:
            #街道编号
            streetNo = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_STREETNO&_dc=1560481030940')
            #社区编号
            commNo = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_COMMNO&_dc=1560481030942')
            #性别
            sex = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=STD_GB_SEX&_dc=1560481031896')
            #对社会影响
            familyEffect = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_FAMILYEFFECT&_dc=1560481063822')
            #治疗情况
            cureCircs = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_CURECIRCS&_dc=1560481063824')
            #目前状况
            nowStatus = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_NOWTONE&_dc=1560481063826')
            #生活料理
            livingCare = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_SOCIETYSTATUS&_dc=1560481063826')
            #家务劳动
            housework = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_SOCIETYSTATUS&_dc=1560481063826')
            #生产劳动
            working = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_SOCIETYSTATUS&_dc=1560481063826')
            #学习能力
            studyAbility = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_SOCIETYSTATUS&_dc=1560481063826')
            #人际交往
            societyHuman = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_SOCIETYSTATUS&_dc=1560481063826')
            #医疗保障
            medicalEnsure = getDict('http://172.28.3.157:8080/xchzz/cenrep/common/loadGeneralCodeCodeLoader.action?codeTableName=GX_DIC_MEDICALENSURE&_dc=1560481063829')


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
                        if item == 'familyEffect' and info[item] in familyEffect:
                            info[item] = familyEffect[info[item]]
                        if item == 'nowStatus' and info[item] in nowStatus:
                            info[item] = nowStatus[info[item]]
                        if item == 'cureCircs' and info[item] in cureCircs:
                            info[item] = cureCircs[info[item]]
                        if item == 'livingCare' and info[item] in livingCare:
                            info[item] = livingCare[info[item]]
                        if item == 'housework' and info[item] in housework:
                            info[item] = housework[info[item]]
                        if item == 'working' and info[item] in working:
                            info[item] = working[info[item]]
                        if item == 'studyAbility' and info[item] in studyAbility:
                            info[item] = studyAbility[info[item]]
                        if item == 'societyHuman' and info[item] in societyHuman:
                            info[item] = societyHuman[info[item]]
                        if item == 'medicalEnsure' and info[item] in medicalEnsure:
                            info[item] = medicalEnsure[info[item]]
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
                                    if item == 'familyEffect' and info[item] in familyEffect:
                                        info[item] = familyEffect[info[item]]
                                    if item == 'nowStatus' and info[item] in nowStatus:
                                        info[item] = nowStatus[info[item]]
                                    if item == 'cureCircs' and info[item] in cureCircs:
                                        info[item] = cureCircs[info[item]]
                                    if item == 'livingCare' and info[item] in livingCare:
                                        info[item] = livingCare[info[item]]
                                    if item == 'housework' and info[item] in housework:
                                        info[item] = housework[info[item]]
                                    if item == 'working' and info[item] in working:
                                        info[item] = working[info[item]]
                                    if item == 'studyAbility' and info[item] in studyAbility:
                                        info[item] = studyAbility[info[item]]
                                    if item == 'societyHuman' and info[item] in societyHuman:
                                        info[item] = societyHuman[info[item]]
                                    if item == 'medicalEnsure' and info[item] in medicalEnsure:
                                        info[item] = medicalEnsure[info[item]]
                                    row[columns[item]] = info[item]
                            writer.writerow(row)
           
getData()






    

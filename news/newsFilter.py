# encoding: utf-8

"""
@author: 王良
@license: Apache Licence
@contact: 744516468@qq.com
@file: newsFilter.py
@time: 2018/12/22 9:49
"""
from pymongo import MongoClient
import xlrd

# 新闻结果过滤处理
regeions = []
caseTypes = []
keywords = []
# 获取区域
book = xlrd.open_workbook('filter/东坝.xlsx')
sheet = book.sheet_by_index(0)
for i in range(0, sheet.nrows):
    value = sheet.cell(i, 0).value.strip()
    if value != '':
        regeions.append(value)
# 获取事件
book = xlrd.open_workbook('filter/昌平区事件分类编码删减.xlsx')
sheet = book.sheet_by_index(1)
for i in range(1, sheet.nrows):
    value = sheet.cell(i, 0).value.strip()
    if value != '':
        caseTypes.append(value)
    value = sheet.cell(i, 1).value.strip()
    if value != '':
        caseTypes.append(value)
# 获取关键字
texts = open('filter/keywords.txt',encoding='utf-8').read().splitlines()
for i in texts:
    keywords.append(i.split(','))
regeions = list(set(regeions))
caseTypes = list(set(caseTypes))
client = MongoClient(host='127.0.0.1', port=27017)
tdb = client['DCS_NEWS']
colNews = tdb['NEWS']
# filter = []
# for regeion in regeions:
#     filter.append({"content": {'$regex': '.' + regeion + '.*'}})
#     filter.append({"leadingTitle": {'$regex': '.' + regeion + '.*'}})
#     filter.append({"mainTitle": {'$regex': '.' + regeion + '.*'}})
#     filter.append({"subTitle": {'$regex': '.' + regeion + '.*'}})
# results = collection.find({'$or': filter})
results = colNews.find()
colCaseNews = tdb['CITYCASE_NEWS']
for result in results:
    # 区域过滤
    for regeion in regeions:
        if regeion in result['content'] or regeion in result['leadingTitle'] or\
                        regeion in result['mainTitle'] or regeion in result['subTitle']:
            index = 0
            cityCase = ''
            # 事件过滤
            for caseType in caseTypes:
                if caseType in result['content'] or caseType in result['leadingTitle'] or \
                                caseType in result['mainTitle'] or caseType in result['subTitle']:
                    index += 1
                    cityCase += ',' + caseType
            if index > 0:
                # 关键字过滤
                for keyword in keywords:
                    isTrue = True
                    for i in keyword:
                        isTrue &= i in result['content']
                    if isTrue:
                        result['caseCount'] = index
                        result['cityCase'] = cityCase[1:]
                        result['keyword'] = keyword
                        result['url'] = 'https://mp.weixin.qq.com'
                        result.pop('_id')
                        print(result)
                        colCaseNews.insert(result)
                        break
            break

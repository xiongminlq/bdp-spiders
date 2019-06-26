# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt
import xlrd
from pymongo import MongoClient


class CompanyPipeline(object):
    def __init__(self):
        self.items = {}
        host = '127.0.0.1'
        port = 27017
        dbName = 'DCS_NEWS'
        client = MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb['QY']

    def process_item(self, item, spider):
        self.items[item['name']] = item
        self.post.insert(dict(item))

    def addCellValue(self, sheet, row, values):
        for i in range(len(values)):
            sheet.write(row, i, values[i])

    def close_spider(self, spider):
        print('*****************************************')
        newBook = xlwt.Workbook(encoding='utf-8')
        sheet1 = newBook.add_sheet('企业信息')
        self.addCellValue(sheet1, 0, ['统一社会信用代码', '组织机构代码', '单位详细名称', '单位所在地-街(村)、门牌号', '单位所在地-社区(居委会)',
                          '联系人', '联系电话', '企业类型', '所属行业', '营业期限', '登记机关', '法人', '成立日期'])
        row = {'exceptions': {'sheet': newBook.add_sheet('经营异常'), 'header': [], 'row': 0},
               'svlist': {'sheet': newBook.add_sheet('严重违法'), 'header': [], 'row': 0},
               'penaltylist': {'sheet': newBook.add_sheet('行政处罚-工商局'), 'header': [], 'row': 0},
               'creditlist': {'sheet': newBook.add_sheet('行政处罚-信用中国'), 'header': [], 'row': 0},
               'otherpunishlist': {'sheet': newBook.add_sheet('行政处罚-其他'), 'header': [], 'row': 0},
               'envlist': {'sheet': newBook.add_sheet('环保处罚'), 'header': [], 'row': 0}}
        book = xlrd.open_workbook('企业数据.xlsx')
        sheet = book.sheet_by_index(0)
        for i in range(1, sheet.nrows):
            name = sheet.cell(i, 2).value.strip()
            # 保存基本信息
            values = [str(sheet.cell(i, 0).value), str(sheet.cell(i, 1).value), str(sheet.cell(i, 2).value),
                      str(sheet.cell(i, 3).value), str(sheet.cell(i, 4).value), str(sheet.cell(i, 5).value), str(sheet.cell(i, 6).value)]
            if name in self.items:
                item = self.items[name]
                values.append(str(item['company_type']) if item['company_type'] else '')
                values.append(str(item['industry_involed']) if item['company_type'] else '')
                values.append(str(item['operate_period']) if item['company_type'] else '')
                values.append(str(item['registration_authority']) if item['company_type'] else '')
                values.append(str(item['corporation']) if item['company_type'] else '')
                values.append(str(item['establishment']) if item['company_type'] else '')
                values[0] = str(item['social_code']) if item['social_code'] else values[0]
                values[1] = str(item['organization_code']) if item['organization_code'] else values[1]
                # 经营异常信息
                risks = item['risk']
                rowindex = 0
                for risk in risks:
                    id = risk['id']
                    if len(risk['data']) > 0 and id in row:
                        wsheet = row[id]['sheet']
                        # 添加企业名称
                        if '企业名称' not in row[id]['header']:
                            wsheet.write(0, 0, '企业名称')
                            row[id]['header'].insert(0, '企业名称')
                        for data in risk['data']:
                            rowindex = row[id]['row'] + 1
                            row[id]['row'] = rowindex
                            wsheet.write(rowindex, 0, name)
                            for j in data:
                                key = j.replace(':', '').replace('：','')
                                value = data[j]
                                colindex = len(row[id]['header'])
                                if key in row[id]['header']:
                                    colindex = row[id]['header'].index(key)
                                else:
                                    wsheet.write(0, colindex, key)
                                    row[id]['header'].append(key)
                                wsheet.write(rowindex, colindex, value)
            self.addCellValue(sheet1, i, values)
        newBook.save('企业信息-结果.xls')

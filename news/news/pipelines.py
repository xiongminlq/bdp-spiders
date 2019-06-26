# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import xlrd
import news.settings as setting
import pymysql
import uuid


class NewsPipeline(object):
    def __init__(self):
        self.resultCount = 0
        self.conn = psycopg2.connect(
            database=setting.database,
            user=setting.user,
            password=setting.password,
            host=setting.host,
            port=setting.port)
        self.cur = self.conn.cursor()
        # 新闻结果过滤处理
        self.regeions = []
        self.caseTypes = []
        self.keywords = []
        # 获取区域
        book = xlrd.open_workbook('filter/东坝.xlsx')
        sheet = book.sheet_by_index(0)
        for i in range(0, sheet.nrows):
            value = sheet.cell(i, 0).value.strip()
            if value != '':
                self.regeions.append(value)
        # 获取事件
        book = xlrd.open_workbook('filter/昌平区事件分类编码删减.xlsx')
        sheet = book.sheet_by_index(1)
        for i in range(1, sheet.nrows):
            value = sheet.cell(i, 0).value.strip()
            if value != '':
                self.caseTypes.append(value)
            value = sheet.cell(i, 1).value.strip()
            if value != '':
                self.caseTypes.append(value)
        # 获取关键字
        texts = open('filter/keywords.txt', encoding='utf-8').read().splitlines()
        for i in texts:
            self.keywords.append(i.split(','))
        self.regeions = list(set(self.regeions))
        self.caseTypes = list(set(self.caseTypes))

    def process_item(self, item, spider):
        newsInfo = dict(item)
        # 区域过滤
        for regeion in self.regeions:
            if regeion in newsInfo['content'] or regeion in newsInfo['leadingTitle'] or \
                    regeion in newsInfo['mainTitle'] or regeion in newsInfo['subTitle']:
                index = 0
                cityCase = ''
                # 事件过滤
                for caseType in self.caseTypes:
                    if caseType in newsInfo['content'] or caseType in newsInfo['leadingTitle'] or \
                            caseType in newsInfo['mainTitle'] or caseType in newsInfo['subTitle']:
                        index += 1
                        cityCase += ',' + caseType
                if index > 0:
                    # 关键字过滤
                    for keyword in self.keywords:
                        isTrue = True
                        for i in keyword:
                            isTrue &= i in newsInfo['content']
                        if isTrue:
                            title = newsInfo['leadingTitle'] + newsInfo['mainTitle'] if 'leadingTitle' in newsInfo else \
                                newsInfo[
                                    'mainTitle']
                            title += newsInfo['subTitle'] if 'subTitle' in newsInfo else ''
                            sql = "SELECT pkid FROM public.yq_hotnews where hot_title='%s' and hot_source='%s';" % (
                                title, newsInfo['source'])
                            self.cur.execute(sql)
                            if len(self.cur.fetchall()) == 0:
                                sql = "insert into yq_hotnews(hot_title,hot_catalog,hot_level,hot_date,hot_abstract,hot_keys,hot_source,hot_url,mongoid) " \
                                      "values('%s','%s',%s,'%s','%s','%s','%s','%s','%s');" % (
                                          title, '', 1, str(newsInfo['date']), newsInfo['content'],
                                          cityCase, newsInfo['source'], newsInfo['url'], '')
                                self.cur.execute(sql)
                                self.resultCount += 1
                            break
                break

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        print("入库数据总数：" + str(self.resultCount))


class NewsPipeline1(object):
    def __init__(self):
        self.resultCount = 0
        self.conn = psycopg2.connect(
            database=setting.database,
            user=setting.user,
            password=setting.password,
            host=setting.host,
            port=setting.port)
        self.cur = self.conn.cursor()
        # 新闻结果过滤处理
        self.regeions = []
        # 获取区域
        book = xlrd.open_workbook('filter/东坝.xlsx')
        sheet = book.sheet_by_index(0)
        for i in range(0, sheet.nrows):
            value = sheet.cell(i, 0).value.strip()
            if value != '':
                self.regeions.append(value)
        self.regeions = list(set(self.regeions))

    def process_item(self, item, spider):
        newsInfo = dict(item)
        # 区域过滤
        for regeion in self.regeions:
            if regeion in newsInfo['content'] or regeion in newsInfo['leadingTitle'] or regeion in newsInfo['mainTitle'] \
                    or regeion in newsInfo['subTitle']:
                title = newsInfo['leadingTitle'] + newsInfo['mainTitle'] if 'leadingTitle' in newsInfo else newsInfo[
                    'mainTitle']
                title += newsInfo['subTitle'] if 'subTitle' in newsInfo else ''
                sql = "SELECT pkid FROM public.yq_hotnews where hot_title='%s' and hot_source='%s';" % (
                    title, newsInfo['source'])
                self.cur.execute(sql)
                if len(self.cur.fetchall()) == 0:
                    sql = "insert into yq_hotnews(hot_title,hot_catalog,hot_level,hot_date,hot_abstract,hot_keys,hot_source,hot_url,mongoid) " \
                          "values('%s','%s',%s,'%s','%s','%s','%s','%s','%s');" % (
                              title, '', 1, str(newsInfo['date']), newsInfo['content'],
                              '', newsInfo['source'], newsInfo['url'], '')
                    self.cur.execute(sql)
                    self.resultCount += 1
                break

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        print("入库数据总数：" + str(self.resultCount))


class RMWLYPipeline(object):
    def __init__(self):
        self.resultCount = 0
        self.conn = psycopg2.connect(
            database=setting.database,
            user=setting.user,
            password=setting.password,
            host=setting.host,
            port=setting.port)
        self.cur = self.conn.cursor()
        self.caseTypes = []
        # 获取事件
        book = xlrd.open_workbook('filter/昌平区事件分类编码删减.xlsx')
        sheet = book.sheet_by_index(1)
        for i in range(1, sheet.nrows):
            value = sheet.cell(i, 0).value.strip()
            if value != '':
                self.caseTypes.append(value)
            value = sheet.cell(i, 1).value.strip()
            if value != '':
                self.caseTypes.append(value)
        self.caseTypes = list(set(self.caseTypes))

    def process_item(self, item, spider):
        newsInfo = dict(item)
        newsInfo['status'] = 1
        # 处理数据存入postgresql数据库
        index = 0
        cityCase = ''
        # 事件过滤
        for caseType in self.caseTypes:
            if caseType in newsInfo['content'] or caseType in newsInfo['mainTitle']:
                index += 1
                cityCase += ',' + caseType
        # 不存在才入库
        title = newsInfo['mainTitle']
        sql = "SELECT pkid FROM public.yq_hotnews where hot_title='%s' and hot_source='%s';" % (
            title, newsInfo['source'])
        self.cur.execute(sql)
        if len(self.cur.fetchall()) == 0:
            sql = "insert into yq_hotnews(hot_title,hot_catalog,hot_level,hot_date,hot_abstract,hot_keys,hot_source,hot_url,mongoid) " \
                  "values('%s','%s',%s,'%s','%s','%s','%s','%s','%s');" % (
                      title, '', 1, str(newsInfo['date']), newsInfo['content'],
                      cityCase, newsInfo['source'], newsInfo['url'], '')
            self.cur.execute(sql)
        self.resultCount += 1

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        print("入库数据总数：" + str(self.resultCount))


class RMWLYPipeline1(object):
    def __init__(self):
        self.resultCount = 0
        self.conn = psycopg2.connect(database=setting.database,
                                     user=setting.user,
                                     password=setting.password,
                                     host=setting.host,
                                     port=setting.port)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        newsInfo = dict(item)
        newsInfo['status'] = 1
        # 不存在才入库
        title = newsInfo['mainTitle']
        sql = "SELECT pkid FROM public.yq_hotnews where hot_title='%s' and hot_source='%s';" % (
            title, newsInfo['source'])
        self.cur.execute(sql)
        if len(self.cur.fetchall()) == 0:
            sql = "insert into yq_hotnews(hot_title,hot_catalog,hot_level,hot_date,hot_abstract,hot_keys,hot_source,hot_url,mongoid) " \
                  "values('%s','%s',%s,'%s','%s','%s','%s','%s','%s');" % (
                      title, '', 1, str(newsInfo['date']), newsInfo['content'],
                      '', newsInfo['source'], newsInfo['url'], '')
            self.cur.execute(sql)
        self.resultCount += 1

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        print("入库数据总数：" + str(self.resultCount))


class WechatPipeline(object):
    def __init__(self):
        # 微信文章由于抓取不准确，需要过滤掉这些关键字后面的内容
        self.end = ['东坝近期重要信息一览', '邻友圈下载方式', '东霸邻友圈公众平台']
        self.resultCount = 0
        self.conn = psycopg2.connect(database=setting.database,
                                     user=setting.user,
                                     password=setting.password,
                                     host=setting.host,
                                     port=setting.port)
        self.cur = self.conn.cursor()
        self.keywords = []
        self.caseTypes = []
        # 获取关键字
        texts = open('filter/w_keywords.txt', encoding='utf-8').read().splitlines()
        for i in texts:
            self.keywords.append(i)
        # 获取事件
        book = xlrd.open_workbook('filter/昌平区事件分类编码删减.xlsx')
        sheet = book.sheet_by_index(1)
        for i in range(1, sheet.nrows):
            value = sheet.cell(i, 0).value.strip()
            if value != '':
                self.caseTypes.append(value)
            value = sheet.cell(i, 1).value.strip()
            if value != '':
                self.caseTypes.append(value)
        self.caseTypes = list(set(self.caseTypes))

    def process_item(self, item, spider):
        newsInfo = dict(item)
        newsInfo['status'] = 1
        # id = self.post.insert(newsInfo)
        # 处理数据存入postgresql数据库
        cityCase = ''
        # 事件过滤
        for caseType in self.caseTypes:
            if caseType in newsInfo['content'] or caseType in newsInfo['mainTitle']:
                cityCase += ',' + caseType
        if cityCase != '':
            cityCase = cityCase[1:]
        # 关键字过滤
        content = newsInfo['content'].replace('\n', '').strip()
        index = 0
        for i in self.end:
            j = content.find(i)
            index = j if j > index else index
        if index > 0:
            content = content[:index]
        print(content)
        for keyword in self.keywords:
            if keyword in content:
                # 不存在才入库
                title = newsInfo['leadingTitle'] + newsInfo['mainTitle'] if 'leadingTitle' in newsInfo else newsInfo[
                    'mainTitle']
                title += newsInfo['subTitle'] if 'subTitle' in newsInfo else ''
                sql = "SELECT pkid FROM public.yq_hotnews where hot_title='%s' and hot_source='%s';" % (
                    title, newsInfo['source'])
                self.cur.execute(sql)
                if len(self.cur.fetchall()) == 0:
                    sql = "insert into yq_hotnews(hot_title,hot_catalog,hot_level,hot_date,hot_abstract,hot_keys,hot_source,hot_url,mongoid) " \
                          "values('%s','%s',%s,'%s','%s','%s','%s','%s','%s');" % (
                              title, '', 1, str(newsInfo['date']), content,
                              cityCase, newsInfo['source'],
                              newsInfo['url'], '')
                    print(sql)
                    self.cur.execute(sql)
                    self.resultCount += 1
                break

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        print("入库数据总数：" + str(self.resultCount))


class WechatPipeline1(object):
    def __init__(self):
        # 微信文章由于抓取不准确，需要过滤掉这些关键字后面的内容
        self.end = ['东坝近期重要信息一览', '邻友圈下载方式', '东霸邻友圈公众平台']
        self.resultCount = 0
        self.conn = psycopg2.connect(database=setting.database,
                                     user=setting.user,
                                     password=setting.password,
                                     host=setting.host,
                                     port=setting.port)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        newsInfo = dict(item)
        newsInfo['status'] = 1
        content = newsInfo['content'].replace('\n', '').strip()
        index = 0
        for i in self.end:
            j = content.find(i)
            index = j if j > index else index
        content = content[:index] if index > 0 else content
        # 不存在才入库
        title = newsInfo['leadingTitle'] + newsInfo['mainTitle'] if 'leadingTitle' in newsInfo else newsInfo[
            'mainTitle']
        title += newsInfo['subTitle'] if 'subTitle' in newsInfo else ''
        sql = "SELECT pkid FROM public.yq_hotnews where hot_title='%s' and hot_source='%s';" % (
            title, newsInfo['source'])
        self.cur.execute(sql)
        if len(self.cur.fetchall()) == 0:
            sql = "insert into yq_hotnews(hot_title,hot_catalog,hot_level,hot_date,hot_abstract,hot_keys,hot_source,hot_url,mongoid) " \
                  "values('%s','%s',%s,'%s','%s','%s','%s','%s','%s');" % (title, '', 1, str(newsInfo['date']), content,
                                                                           '', newsInfo['source'], newsInfo['url'], '')
            self.cur.execute(sql)
            self.resultCount += 1

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        print("入库数据总数：" + str(self.resultCount))


class XCZZPipeline(object):
    def __init__(self):
        self.resultCount = 0
        # 打开数据库连接
        self.db = pymysql.Connect(
            host='10.161.236.143',
            port=3306,
            user='root',
            passwd='supermap',
            db='freecms',
            charset='utf8')
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()
        self.htmlIndexnum = -1
        sql = "select min(htmlIndexnum) as htmlIndexnum from freecms_info where htmlIndexnum<0"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None and len(result) > 0 and result[0] is not None:
            self.htmlIndexnum = int(result[0]) - 1

    def process_item(self, item, spider):
        newsInfo = dict(item)
        # 不存在才入库
        sql = "SELECT id FROM freecms_info where title='%s' and source='%s';" % (
            newsInfo['mainTitle'], newsInfo['source'])
        self.cursor.execute(sql)
        if len(self.cursor.fetchall()) == 0:
            shortTitle = newsInfo['subTitle'] if 'subTitle' in newsInfo else ''
            sql = "insert into freecms_info(id,site,channel,title,shortTitle,titleColor,titleBlod,source,author," \
                  "description,content,addtime,templet,isHot,isTop,clickNum,addUser,issign,iscomment,opentype,opentimetype," \
                  "htmlIndexnum,url) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s," \
                  "'%s','%s','%s','%s','%s',%s,'%s');" % (str(uuid.uuid1()), newsInfo['site'], newsInfo['edition'],
                                                          newsInfo['mainTitle'], shortTitle, '000000', '0',
                                                          newsInfo['source'],
                                                          newsInfo['anthor'], '', newsInfo['content'],
                                                          str(newsInfo['date']),
                                                          'newsInfo.html', '0', '0', 0,
                                                          '02debc9f-53cd-4bc9-887b-49ffc4e925f2',
                                                          '0', '0', '1', '1', self.htmlIndexnum, newsInfo['url'])
            self.cursor.execute(sql)
        self.resultCount += 1
        self.htmlIndexnum -= 1

    def close_spider(self, spider):
        self.db.commit()
        # 关闭数据库连接
        self.db.close()
        print("入库数据总数：" + str(self.resultCount))


class NewsPipeline2(object):

    def process_item(self, item, spider):
        return item

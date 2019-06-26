# encoding: utf-8

"""
@author: 王良
@license: Apache Licence
@contact: 744516468@qq.com
@file: mongodb2postgresql.py
@time: 2018/12/26 20:36
"""

from pymongo import MongoClient
import psycopg2

client = MongoClient(host='127.0.0.1', port=27017)
tdb = client['DCS_NEWS']
colCaseNews = tdb['CITYCASE_NEWS']
results = colCaseNews.find()
conn = psycopg2.connect(database="grid_yq", user="grid_yq", password="mapapp", host="192.168.46.237", port="5432")
cur = conn.cursor()
index =0
for result in results:
    index += 1
    title = result['leadingTitle'] + result['mainTitle'] if 'leadingTitle' in result else result['mainTitle']
    title += result['subTitle'] if 'subTitle' in result else ''
    sql = "insert into yq_hotnews(hot_title,hot_catalog,hot_level,hot_date,hot_abstract,hot_keys,hot_source,hot_url,mongoid) " \
          "values('%s','%s',%s,'%s','%s','%s','%s','%s','%s');" %(title,'',1,str(result['date']),'',
                result['cityCase'],result['source'], result['url'], str(result['_id']))
    cur.execute(sql)
conn.commit()
conn.close()
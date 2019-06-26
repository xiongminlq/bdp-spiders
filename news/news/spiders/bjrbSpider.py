# -*- coding: utf-8 -*-
from news.spiders.bjwbSpider import BjwbSpider
import datetime


class BjrbSpider(BjwbSpider):
    name = 'bjrb'
    allowed_domains = ['bjrb.bjd.com.cn']
    # 2017-01/01
    start_urls = []

    def __init__(self):
        url_template = 'http://bjrb.bjd.com.cn/html/{0}/node_1.htm'
        # startDate = datetime.datetime(2018, 12, 23)
        endDate = datetime.datetime.now()
        # while startDate <= endDate:
        #     self.start_urls.append(url_template.format(startDate.strftime('%Y-%m/%d')))
        #     startDate += datetime.timedelta(days=1)
        self.start_urls.append(url_template.format(endDate.strftime('%Y-%m/%d')))

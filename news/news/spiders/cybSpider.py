# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import datetime


class CybSpider(scrapy.Spider):
    name = 'cyb'
    allowed_domains = ['video.bjchy.gov.cn']
    # 2017-01/01
    start_urls = []

    def __init__(self):
        url_template = 'http://video.bjchy.gov.cn/vodfiles/992/2015/09/23/cyb/html/{0}/node_1.htm'
        self.endDate = datetime.datetime.now()
        self.start_urls.append(url_template.format(self.endDate.strftime('%Y-%m/%d')))


    def parseContent(self, response):
        item = NewsItem()
        mainTitle = response.xpath('/html/body/table/tr[1]/td[2]/table[2]/tr/td/table/tr[2]/td/div/'
                             'table/tr[1]/td/table/tbody').xpath('string()').extract_first()
        datetext = response.url[response.url.rindex('html/') + 5:response.url.rindex('/')]
        content = response.xpath('//div[@id="ozoom"]').xpath('string()').extract_first()
        edition = response.xpath('/html/body/table/tr[1]/td[1]/table/tr[1]/td/'
                                 'table[2]/tr/td[2]').xpath('string()').extract_first()
        item['leadingTitle'] = ''
        item['mainTitle'] = mainTitle.replace('\r', '').replace('\n', '').replace('\t', '') \
            .replace('\xa0', ' ').replace('\u3000', ' ').strip()
        item['subTitle'] = ''
        item['source'] = '朝阳报'
        date = ''
        try:
            date = self.endDate
        except:
            print('时间转换失败')
        item['date'] = date
        item['edition'] = edition.replace('\r', '').replace('\n', '') \
            .replace('\xa0', ' ').replace('\u3000', ' ').strip()
        item['anthor'] = ''
        item['content'] = content.replace('\r', '').replace('\n', '') \
            .replace('\xa0', ' ').replace('\u3000', ' ').strip()
        item['url'] = response.url
        yield item

    def parse(self, response):
        url = response.url[:response.url.rindex('/') + 1]
        # 获取新闻正文url
        area_selects = response.xpath('//map[@name="PagePicMap"]')
        if area_selects is not None:
            for area_select in area_selects:
                contenthtm = area_select.xpath('./area/@href').extract_first()
                if contenthtm is not None:
                    contenthtm = url + contenthtm
                yield scrapy.Request(response.urljoin(contenthtm), callback=self.parseContent)
        #获取下一版
        next = response.xpath('//a[@class="preart"]')
        if next is not None:
            for i in next:
                if '下一版' == i.xpath('./text()').extract_first().strip():
                    nextUrl = url + i.xpath('./@href').extract_first()
                    yield scrapy.Request(response.urljoin(nextUrl))
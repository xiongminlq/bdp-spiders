# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import datetime


class FzwbSpider(scrapy.Spider):
    name = 'fzwb'
    allowed_domains = ['dzb.fawan.com']
    # 2011-12/01
    start_urls = []

    def __init__(self):
        url_template = 'http://dzb.fawan.com/html/{0}/node_2.htm'
        startDate = datetime.datetime(2011, 12, 1)
        endDate = datetime.datetime.now()
        while startDate <= endDate:
            self.start_urls.append(url_template.format(startDate.strftime('%Y-%m/%d')))
            startDate += datetime.timedelta(days=1)

    def parse(self, response):
        if 'node' in response.url:
            url = response.url[:response.url.rindex('/') + 1]
            # 第一页为要闻导航，过滤掉
            if not response.url.endswith('node_2.htm'):
                # 获取新闻正文url
                area_selects = response.xpath('//map[@name="pagepicmap"]/area')
                if area_selects is not None:
                    for area_select in area_selects:
                        contenthtm = area_select.xpath('./@href').extract_first()
                        if contenthtm is not None:
                            contenthtm = url + contenthtm
                            yield scrapy.Request(response.urljoin(contenthtm))
            # 获取下一版
            nextUrl= None
            if response.url.endswith('node_2.htm'):
                nextUrl = response.xpath('//span[@class="pagebar"]/font/table/tbody/tr/td/div/a/@href').extract_first()
            else:
                nextUrl = response.xpath('//span[@class="pagebar"]/font/table/tbody/tr/td/div/a[2]/@href').extract_first()
            if nextUrl is not None:
                nextUrl = url + nextUrl
                yield scrapy.Request(response.urljoin(nextUrl))
        # 获取新闻内容，包括标题、来源、日期、作者、版次
        elif 'content' in response.url:
            item = NewsItem()
            leadingTitle =response.xpath('//*[@id="Table_01"]/tr[2]/td[2]/table/tr[1]/td/table/tbody/tr/td/span[1]/text()').extract_first()
            mainTitle = response.xpath('//*[@id="Table_01"]/tr[2]/td[2]/table/tr[1]/td/table/tbody/tr/td/strong/text()').extract_first()
            subTitle = response.xpath('//*[@id="Table_01"]/tr[2]/td[2]/table/tr[1]/td/table/tbody/tr/td/span[2]/text()').extract_first()
            edition = response.xpath('//*[@id="Table_"]/tr[2]/td[2]/table/tr/td[3]/text()').extract_first()
            # 从URL中获取日期
            date = response.url[26:36]
            item['leadingTitle'] = '' if leadingTitle is None else leadingTitle.replace('\r','').replace('\n','').replace('\t','') \
                .replace('\xa0', ' ').replace('\u3000', ' ').strip()
            item['mainTitle'] = '' if mainTitle is None else mainTitle.replace('\r','').replace('\n','').replace('\t','') \
                .replace('\xa0', ' ').replace('\u3000', ' ').strip()
            item['subTitle'] = '' if subTitle is None else subTitle.replace('\r','').replace('\n','').replace('\t','') \
                .replace('\xa0', ' ').replace('\u3000', ' ').strip()
            item['source'] = '法制晚报'
            try:
                item['date'] = datetime.datetime.strptime(date.strip(), '%Y-%m/%d')
            except:
                pass
            item['edition'] = '' if edition is None else edition.replace("版次：","").replace('\r','').replace('\n','') \
                .replace('\xa0', ' ').replace('\u3000', ' ').strip()
            item['anthor'] = ''
            text = response.xpath('//*[@id="ozoom"]')
            content = ''
            if text is not None:
                text = text.xpath('string()').extract_first()
                if text is not None:
                    content += text.replace('\xa0', ' ').replace('\u3000', ' ')
            item['content'] = content
            yield item
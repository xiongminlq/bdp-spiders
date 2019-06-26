# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import datetime


class ChinapeaceSpider(scrapy.Spider):
    name = 'chinapeace'
    allowed_domains = ['www.chinapeace.gov.cn']
    custom_settings = {
        'ITEM_PIPELINES': {'news.pipelines.XCZZPipeline': 311, },
        'DOWNLOAD_DELAY': 0.5
    }
    start_urls = ['http://www.chinapeace.gov.cn/node_54299.htm', 'http://www.chinapeace.gov.cn/node_54302.htm',
                  'http://www.chinapeace.gov.cn/node_54303.htm', 'http://www.chinapeace.gov.cn/node_54230.htm',
                  'http://www.chinapeace.gov.cn/node_54300.htm', 'http://www.chinapeace.gov.cn/node_54301.htm',
                  'http://www.chinapeace.gov.cn/node_54324.htm', 'http://www.chinapeace.gov.cn/node_54325.htm',
                  'http://www.chinapeace.gov.cn/node_54326.htm', 'http://www.chinapeace.gov.cn/node_54327.htm',
                  'http://www.chinapeace.gov.cn/node_54328.htm']
    ids = {'综合治理': 'e652b5c0-f02f-45c2-90a3-643ab1e9dcad',
           '平安建设': 'e652b5c0-f02f-45c2-90a3-643ab1e9dcad',
           '队伍建设': '2cf1d5bc-4e77-434d-bb6c-a775655066cd',
           '文化': '2cf1d5bc-4e77-434d-bb6c-a775655066cd',
           '司法改革': '56550bde-1362-4bff-b6b1-6210e9bab646',
           '法治建设': '56550bde-1362-4bff-b6b1-6210e9bab646',
           '政法工作': '56550bde-1362-4bff-b6b1-6210e9bab646'}
    base_url = 'http://www.chinapeace.gov.cn/'
    headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }

    def parseContent(self, response):
        item = NewsItem()
        item['leadingTitle'] = ''
        item['source'] = '中国长安网'
        item['edition'] = response.meta['channel']
        item['date'] = response.meta['date']
        item['url'] = response.url
        item['site'] = 'a76304d3-3ee0-47f2-8077-a2d08e2b7333'
        title = response.xpath('//div[@class="content-l fl"]/h1/text()').extract_first()
        item['mainTitle'] = '' if title is None else title. \
            replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
        source = response.xpath('//div[@class="source"]/text()').extract_first()\
            .replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
        index = source.find('责任编辑')
        if index > 0:
            item['anthor'] = source[index + 5:].replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
        # index = source.find('来源')
        # if index > 0:
        #     date = source[:index].replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
        #     try:
        #         item['date'] = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        #     except:
        #         pass
        item['date'] = response.meta['date']
        content = response.xpath('//div[@class="content-main"]').xpath('string()').extract_first()
        item['content'] = '' if content is None else content.\
            replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
        yield item

    def parse(self, response):
        channel = response.xpath('//div[@class="position"]/a[2]/text()').extract_first()
        if channel is not None:
            channelId = self.ids[channel] if channel in self.ids else None
            news = response.xpath('//div[@class="gc-news-list"]/ul/li')
            for new in news:
                href = new.xpath('./a/@href').extract_first()
                if href is not None:
                    # title = new.xpath('./a/text()').extract_first()
                    date = new.xpath('./span/text()').extract_first()
                    try:
                        date = datetime.datetime.strptime(date.strip(), '%Y-%m-%d')
                    except:
                        pass
                    nextUrl = self.base_url + href
                    yield scrapy.Request(response.urljoin(nextUrl),
                                         callback=self.parseContent,
                                         meta={'channel': channelId, 'date': date})
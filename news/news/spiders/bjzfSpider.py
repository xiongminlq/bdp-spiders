# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import datetime


class BjzfSpider(scrapy.Spider):
    name = 'bjzf'
    allowed_domains = ['www.bj148.org']
    custom_settings = {
        'ITEM_PIPELINES': {'news.pipelines.XCZZPipeline': 311, },
        'DOWNLOAD_DELAY': 0.5
    }
    start_urls = ['http://www.bj148.org/']
    ids = {'政法': '56550bde-1362-4bff-b6b1-6210e9bab646',
           '综治': 'e652b5c0-f02f-45c2-90a3-643ab1e9dcad',
           '政工': '2cf1d5bc-4e77-434d-bb6c-a775655066cd',
           '创新': 'e03420fa-baee-4f3d-8040-f60c2f6e48fb'}
    base_url = 'http://www.bj148.org/'
    headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }

    def parseContent(self, response):
        item = NewsItem()
        page = response.xpath('//*[@id="pagebody_left"]')
        if page is not None:
            mainTitle = page.xpath('./h2/text()').extract_first()
            item['mainTitle'] = '' if mainTitle is None else mainTitle.\
                replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
            subTitle = page.xpath('./h3/text()').extract_first()
            item['subTitle'] = '' if subTitle is None else subTitle. \
                replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
            info = page.xpath('./h4/text()').extract_first()
            info = info. replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
            index = info.find('作者')
            if index > 0:
                item['anthor'] = info[index+3:].replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
                info = info[:index]
            index = info.find('来源')
            if index > 0:
                info = info[:index]
            date = info[7:].replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()[1:-1]
            try:
                item['date'] = datetime.datetime.strptime(date.strip(), '%Y-%m-%d')
            except:
                pass
            item['leadingTitle'] = ''
            item['source'] = '北京政法网'
            item['edition'] = response.meta['channel']
            item['url'] = response.url
            item['site'] = 'a76304d3-3ee0-47f2-8077-a2d08e2b7333'
            doucument = response.xpath('//*[@id="doucument"]')
            content = doucument.xpath('./div')
            if content is None:
                content = doucument.xpath('./p').xpath('string()').extract_first()
            else:
                content = content.xpath('string()').extract_first()
            item['content'] = '' if content is None else content.\
                replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
        yield item

    def parseChannel(self, response):
        infolist = response.xpath('//*[@id="lanmucenter"]/div')
        channelId = response.meta['channel']
        if len(infolist) > 0:
            list = infolist.xpath('./div')
            if len(list) > 0:
                for info in list:
                    href = info.xpath('./a/@href').extract_first()
                    title = info.xpath('./a/text()').extract_first()
                    if href is not None:
                        yield scrapy.Request(response.urljoin(response.url + href[2:]),
                                             callback=self.parseContent,
                                             meta={'channel': channelId})
            else:
                infolist = infolist.xpath('./ul/li')
                if len(infolist) > 0:
                    for info in infolist:
                        href = info.xpath('./a/@href').extract_first()
                        title = info.xpath('./a/text()').extract_first()
                        if href is not None:
                            yield scrapy.Request(response.urljoin(response.url + href[2:]),
                                                 callback=self.parseContent,
                                                 meta={'channel': channelId})
        else:
            table = response.xpath('//table[@class="mar12"]/tr/td[3]')
            if len(table) > 0:
                infolist = table.xpath('./div')
                if len(infolist) > 0:
                    for info in infolist:
                        href = info.xpath('./h1/a/@href').extract_first()
                        if href is None:
                            list = info.xpath('./ul/li')
                            if len(list) > 0:
                                for li in list:
                                    href = li.xpath('./a/@href').extract_first()
                                    if href is not None:
                                        yield scrapy.Request(response.urljoin(response.url + href[2:]),
                                                             callback=self.parseContent,
                                                             meta={'channel': channelId})
                        else:
                            yield scrapy.Request(response.urljoin(response.url + href[2:]),
                                                 callback=self.parseContent,
                                                 meta={'channel': channelId})
                else:
                    infolist = table.xpath('./ul')
                    if len(infolist) >0:
                        for info in infolist:
                            list = info.xpath('li')
                            if len(list) > 0:
                                for li in list:
                                    href = li.xpath('./a/@href').extract_first()
                                    if href is not None:
                                        yield scrapy.Request(response.urljoin(response.url + href[2:]),
                                                             callback=self.parseContent,
                                                             meta={'channel': channelId})

    def parse(self, response):
        channels = response.xpath('//div[@class="navbox"]')
        for channel in channels:
            channelName = channel.xpath('./div[1]/strong/a/text()').extract_first().\
                replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
            channelId = self.ids[channelName] if channelName in self.ids else None
            if channelId is not None:
                list = channel.xpath('./div[2]/div')
                for li in list:
                    sub = li.xpath('./a')
                    for s in sub:
                        href = s.xpath('./@href').extract_first()
                        # name = s.xpath('./text()').extract_first()
                        nextUrl = self.base_url + href[2:]
                        yield scrapy.Request(response.urljoin(nextUrl), callback=self.parseChannel,
                                             meta={'channel': channelId})
# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import datetime


class XchzfzzSpider(scrapy.Spider):
    name = 'xchzfzz'
    allowed_domains = ['zfzz.bjxch.gov.cn']
    custom_settings = {
        'ITEM_PIPELINES': {'news.pipelines.XCZZPipeline': 311, },
        'DOWNLOAD_DELAY': 0.5
    }
    start_urls = ['http://zfzz.bjxch.gov.cn/']
    ids = {'/zf.html': '56550bde-1362-4bff-b6b1-6210e9bab646',
           '/zz.html': 'e652b5c0-f02f-45c2-90a3-643ab1e9dcad',
           '/zg.html': '2cf1d5bc-4e77-434d-bb6c-a775655066cd',
           '/cx.html': 'e03420fa-baee-4f3d-8040-f60c2f6e48fb',
           '/fxyj/gzdt.html': '7d6f1153-6bbf-485b-a56c-cff70797ad3c'}
    base_url = 'http://zfzz.bjxch.gov.cn'
    headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }

    def parseContent(self, response):
        item = NewsItem()
        item['leadingTitle'] = ''
        item['mainTitle'] = response.meta['title']
        item['subTitle'] = ''
        item['source'] = '北京西城政法综治网'
        item['date'] = response.meta['date']
        item['edition'] = response.meta['channel']
        item['anthor'] = ''
        item['content'] = response.xpath('//div[@class="xiangqing"]').xpath('string()').extract_first().\
            replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
        item['url'] = response.url
        item['site'] = 'a76304d3-3ee0-47f2-8077-a2d08e2b7333'
        yield item

    def parseChannel(self, response):
        infolist = response.xpath('//div[@class="infolist"]/ul/li')
        channelName = response.meta['channel']
        if infolist is not None:
            for info in infolist:
                title = info.xpath('./a/text()').extract_first()
                title = '' if title is None else title.\
                    replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
                nextUrl = self.base_url + info.xpath('./a/@href').extract_first()
                date = info.xpath('./span/text()').extract_first()
                date = datetime.datetime.strptime(date.strip(), '%Y-%m-%d')
                yield scrapy.Request(response.urljoin(nextUrl), callback=self.parseContent,
                                     meta={'channel': channelName, 'title': title, 'date': date})

    def parse(self, response):
        channels = response.xpath('//div[@class="dh"]/ul/li')
        if channels is not None:
            for channel in channels:
                href = channel.xpath('./a/@href').extract_first()
                channelId = self.ids[href] if href in self.ids else None
                list = channel.xpath('./ul/li')
                if list is not None:
                    for li in list:
                        href = li.xpath('./a/@href').extract_first()
                        nextUrl = self.base_url + href
                        if channelId is None:
                            id = self.ids[href] if href in self.ids else None
                            if id is not None:
                                yield scrapy.Request(response.urljoin(nextUrl), callback=self.parseChannel,
                                                     meta={'channel': id})
                        else:
                            yield scrapy.Request(response.urljoin(nextUrl), callback=self.parseChannel,
                                                 meta={'channel': channelId})
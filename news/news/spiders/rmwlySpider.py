# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import json
import time


class RmwlySpider(scrapy.Spider):
    name = 'rmwly'
    allowed_domains = ['liuyan.people.com.cn']
    custom_settings = {
        'ITEM_PIPELINES': {'news.pipelines.RMWLYPipeline1': 301, },
        'DOWNLOAD_DELAY': 0.5
    }
    start_urls = ['http://liuyan.people.com.cn/threads/search?lastItem=0&queryType=2&keywords=%E4%B8%9C%E5%9D%9D&timeRange=0&fid=539',
                  'http://liuyan.people.com.cn/threads/search?lastItem=0&queryType=2&keywords=%E4%B8%9C%E5%9D%9D&timeRange=0&fid=540',
                  'http://liuyan.people.com.cn/threads/search?lastItem=0&queryType=2&keywords=%E4%B8%9C%E5%9D%9D&timeRange=0&fid=741',
                  'http://liuyan.people.com.cn/threads/search?lastItem=0&queryType=2&keywords=%E4%B8%9C%E5%9D%9D&timeRange=0&fid=742']
    base_url = 'http://liuyan.people.com.cn/threads'
    next_url_template = 'http://liuyan.people.com.cn/threads/search?lastItem={0}&queryType=2&keywords=%E4%B8%9C%E5%9D%9D&timeRange=0'
    content_url_template = 'http://liuyan.people.com.cn/threads/content?tid={0}'
    headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }

    def parseContent(self, response):
        item = NewsItem()
        title = response.xpath('//div[@class="liuyan_box03 w1200 clearfix"]/h2/b/text()').extract_first()
        content = response.xpath('//div[@class="liuyan_box03 w1200 clearfix"]/p').xpath('string()').extract_first()
        item['leadingTitle'] = ''
        item['mainTitle'] = title.replace('\r', '').replace('\n', '').replace('\t', '') \
            .replace('\xa0', ' ').replace('\u3000', ' ').strip()
        item['subTitle'] = ''
        item['source'] = '人民网地方领导留言板'
        item['date'] = response.meta['date']
        item['edition'] = ''
        item['anthor'] = ''
        item['content'] = content.replace('\r', '').replace('\n', '') \
            .replace('\xa0', ' ').replace('\u3000', ' ').strip()
        item['url'] = response.url
        yield item

    def parse(self, response):
        rs = json.loads(response.text)
        if rs['result'] == 'success':
            rows = rs['responseData']['rows']
            tid = ''
            for row in rows:
                tid = row['tid']
                date = time.strftime("%Y-%m-%d", time.localtime(row['dateline']))
                # date = time.localtime(row['dateline'])
                content_url = self.content_url_template.format(tid)
                yield scrapy.Request(response.urljoin(content_url),
                                     callback=self.parseContent,
                                     dont_filter=True,
                                     headers=self.headers,
                                     meta={'date': date})

            # # 翻页
            # next_url = self.next_url_template.format(tid)
            # yield scrapy.Request(response.urljoin(next_url), dont_filter=True, headers=self.headers)

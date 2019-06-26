# encoding: utf-8

"""
@author: 王良
@license: Apache Licence
@contact: 744516468@qq.com
@file: weChatSpier.py
@time: 2019/3/8 9:21
"""

import scrapy
from news.items import NewsItem
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
from datetime import datetime


class WechatSpider(scrapy.Spider):
    name = 'wechat'
    allowed_domains = ['mp.weixin.qq.com']
    custom_settings = {
        'ITEM_PIPELINES': {'news.pipelines.WechatPipeline1': 302, },
        'DOWNLOADER_MIDDLEWARES': {'news.middlewares.SeleniumMiddleware': 501, },
        'DOWNLOAD_DELAY': 5
    }
    headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    cookieDict = {}

    def __init__(self):
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        )
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = user_agent
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver.set_page_load_timeout(30)
        self.driver.set_window_size(800, 600)

    def close(spider, reason):
        spider.driver.close()
        # closed = getattr(spider, 'closed', None)
        # if callable(closed):
        #     return closed(reason)

    def start_requests(self):
        # 获取URL
        text = 'news/spiders/request.txt'
        with open(text, 'r') as f:
            re = json.loads(f.read())
            start_url = 'https://' + re['url']
            cookie = re['cookie']
            items = cookie.split(';')
            if len(items) >1:
                for item in items:
                    key = item.split('=')[0].replace(' ', '')
                    value = item.split('=')[1]
                    self.cookieDict[key] = value
        print('-----------------------------------------')
        print(start_url)
        yield scrapy.Request(url=start_url,
                             headers=self.headers,
                             cookies=self.cookieDict,
                             meta={'usedSelenium': True})

    def parseDetail(self, response):
        item = NewsItem()
        source = response.xpath('//*[@id="js_name"]/text()').extract_first()
        source = '' if source is None else source.replace('\r', '').replace('\n', '').replace('\t', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        sections = response.xpath('//div[@id="js_content"]/*')
        content = ''
        if sections is not None:
            for i in range(len(sections)):
                # 过滤掉无效信息
                if i == 0 or i == 1:
                    continue
                content += sections[i].xpath('string()').extract_first().replace('\r', '').replace('\n', '') \
                    .replace('\t', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
        item['mainTitle'] = ''
        item['mainTitle'] = response.meta['title']
        item['subTitle'] = ''
        item['source'] = source
        item['date'] = datetime.strptime(response.meta['date'].strip(), '%Y年%m月%d日')
        item['anthor'] = source
        item['content'] = content
        item['url'] = response.url
        yield item

    def parse(self, response):
        for media in response.xpath('//div[@class="weui_media_bd js_media"]'):
            title = media.xpath('./h4/text()').extract_first().strip()
            url = media.xpath('./h4/@hrefs').extract_first()
            date = media.xpath('./p[2]/text()').extract_first()
            yield response.follow(url, callback=self.parseDetail,
                                  headers=self.headers,
                                  meta={'title': title, 'date': date, 'usedSelenium': True})

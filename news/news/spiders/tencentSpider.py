# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re


class tencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['qq.com']
    base_url = 'http://bj.jjj.qq.com'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'news.middlewares.SeleniumMiddleware': 502, },
        'DOWNLOAD_DELAY': 5
    }
    headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    def __init__(self):
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        )
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = user_agent
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver.set_page_load_timeout(30)
        self.driver.set_window_size(1920, 1080)

    def start_requests(self):
        start_url = 'http://bj.jjj.qq.com/'
        yield scrapy.Request(url=start_url, headers=self.headers, meta={'usedSelenium': True})

    def close(spider, reason):
        spider.driver.close()

    def parseContent(self, response):
        item = NewsItem()
        item['leadingTitle'] = ''
        item['subTitle'] = ''
        item['source'] = '腾讯新闻'
        item['edition'] = ''
        item['anthor'] = ''
        item['url'] = response.url
        content = response.xpath('//div[@class="LEFT"]')
        if len(content) == 0:
            content = response.xpath('//div[@class="qq_article"]')
            title = content.xpath('./div[1]/h1/text()').extract_first()
            item['mainTitle'] = '' if title is None else title.replace('\r', '').replace('\n', ''). \
                replace('\xa0', ' ').replace('\u3000', ' ').strip()
            date = ''
            './div[1]/div/div[1]/span[2]/text()'
            datetext = response.xpath('//div[@class="a_Info"]/span[@class="a_time"]/text()').extract_first()
            if datetext is not None:
                datetext = datetext.replace('\r', '').replace('\n', '').replace('\xa0', ' ').\
                    replace('\u3000', ' ').strip()
                try:
                    date = datetime.datetime.strptime(datetext.strip(), "%Y-%m-%d %H:%M")
                except:
                    pass
            item['date'] = date
            content = content.xpath('//div[@class="Cnt-Main-Article-QQ"]').xpath('string()').extract_first()
            item['content'] = '' if content is None else content.replace('\r', '').replace('\n', ''). \
                replace('\xa0', ' ').replace('\u3000', ' ').strip()
        else:
            title = content.xpath('./h1/text()').extract_first()
            item['mainTitle'] ='' if title is None else title.replace('\r', '').replace('\n', '').\
                replace('\xa0', ' ').replace('\u3000', ' ').strip()
            date = ''
            datetext = response.xpath('//div[@class="a-src-time"]/a').xpath('string()').extract_first()
            if datetext is not None:
                datetext = datetext.replace('\r', '').replace('\n', '').replace('\xa0', ' ').\
                    replace('\u3000', ' ').strip()
                result = re.findall("(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})", datetext)
                date = result[0] if len(result) > 0 else ''
                try:
                    date = datetime.datetime.strptime(date.strip(), "%Y-%m-%d %H:%M:%S")
                except:
                    print('时间转换失败')
            item['date'] = date
            content = content.xpath('//div[@class="content-article"]').xpath('string()').extract_first()
            item['content'] = '' if content is None else content.replace('\r', '').replace('\n', '').\
                replace('\xa0', ' ').replace('\u3000', ' ').strip()
        yield item

    def parse(self, response):
        newsitem = response.xpath('//div[@class="newsitem"]')
        for item in newsitem:
            url = item.xpath('./a/@href').extract_first()
            if url is not None and url.startswith('/'):
                url = self.base_url + url
            yield response.follow(url, callback=self.parseContent, meta={'usedSelenium': True})

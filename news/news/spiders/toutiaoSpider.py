# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from news.items import NewsItem
import datetime
import re


class ToutiaospiderSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['toutiao.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'news.middlewares.SeleniumMiddleware': 502, },
        'ITEM_PIPELINES': {'news.pipelines.NewsPipeline2': 311, },
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

        # 动态渲染网页初始url_热点新闻
    def start_requests(self):
        start_url = 'https://www.toutiao.com/ch/news_hot/'
        yield scrapy.Request(url=start_url, headers=self.headers, meta={'usedSelenium': True})

    def close(spider, reason):
        spider.driver.close()

    def parseContent(self, response):
        #新闻内容信息获取
        item = NewsItem()
        item['leadingTitle'] = ''
        item['subTitle'] = ''
        item['source'] = '今日头条'
        item['edition'] = ''
        item['anthor'] = ''
        item['url'] = response.url
        #新闻标题
        title = response.xpath('//h1[@class="article-title"]/text()').extract_first()
        item['mainTitle'] = '' if title is None else title.replace('\r', '').replace('\n', '').replace('\t', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        #新闻来源和时间
        list = response.xpath('//div[@class="article-sub"]/span')
        item['pre_source'] = list[1].xpath('string()').extract_first()
        if len(list) > 0:
            datetext = list[-1].xpath('string()').extract_first()
        if len(list) >1:
            pre_source = list[-2].xpath('string()').extract_first()
        item['pre_source'] = '' if pre_source is None else pre_source.replace('\r', '').replace('\n', '').replace('\t', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        date = ''
        if datetext is not None:
            datetext = datetext.replace('\r', '').replace('\n', '').replace('\xa0', ' '). \
                        replace('\u3000', ' ').strip()
            result = re.findall("(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})", datetext)
            date = result[0] if len(result) > 0 else ''
            try:
                date = datetime.datetime.strptime(date.strip(), "%Y-%m-%d %H:%M:%S")
            except:
                print('时间转换失败')
        item['date'] = date
        #新闻内容
        content = response.xpath('//div[@class="article-box"]/div[2]').xpath('string()').extract_first()
        item['content'] = '' if content is None else content.replace('\r', '').replace('\n', '').replace('\t', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        yield item

    def parse(self, response):
        #获取新闻网页列表
        news = response.xpath('//li[@class="item    "]')
        for new in news:
            url = new.xpath('./div/div[1]/div/div/a/@href').extract_first()
            if url is not None:
                url = "https://www.toutiao.com" + str(url).replace('group/', 'a')
                yield response.follow(url, callback=self.parseContent, headers=self.headers,
                                      meta={'usedSelenium': True})


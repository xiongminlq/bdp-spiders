# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from news.items import NewsItem
import datetime


class WyspiderSpider(scrapy.Spider):
    name = 'wy'
    allowed_domains = ['3g.163.com']
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

     #动态渲染网页初始url
    def start_requests(self):
        start_url = 'https://3g.163.com/touch/news/subchannel/domestic/'
        yield scrapy.Request(url=start_url, headers=self.headers, meta={'usedSelenium': True})

    def close(spider, reason):
        spider.driver.close()

    def parseContent(self, response):
        item = NewsItem()
        item['leadingTitle'] = ''
        item['subTitle'] = ''
        #根据爬虫爬虫的新闻类型进行固定
        item['source'] = '网易新闻'
        item['anthor'] = ''
        item['url'] = response.url
        #获取新闻标题，并进行格式化处理
        head = response.xpath('//div[@class="head"]')
        title = head.xpath('./h1/text()').extract_first()
        item['mainTitle'] = '' if title is None else title.replace('\r', '').replace('\n', '').replace('\t', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        #获取新闻时间，并进行格式化处理
        datetext = head.xpath('./div/span[1]/text()').extract_first()
        date = ''
        if datetext is not None:
            datetext = datetext.replace('\r', '').replace('\n', '').replace('\xa0', ' '). \
                replace('\u3000', ' ').strip()
            try:
                date = datetime.datetime.strptime(datetext.strip(), "%Y-%m-%d %H:%M")
            except:
                print('时间转换失败。')
        item['date'] = date
        #新闻引用来源，并进行格式化处理
        pre_source = head.xpath('./div/span[2]/text()').extract_first()
        item['pre_source'] = '' if pre_source is None else pre_source.replace('\r', '').replace('\n', '').replace('\t', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        #新闻内容，并进行格式化处理
        content = response.xpath('//div[@class="content"]/div').xpath('string()').extract_first()
        item['content'] = '' if content is None else content.replace('\r', '').replace('\n', '').replace('\t', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        yield item

    def parse(self, response):
        #获取新闻网页列表
        news = response.xpath('//article[@class="news-card card-type-news"]')
        #获取每一条新闻的url
        for new in news:
            url = new.xpath('./a/@href').extract_first()
            if url is not None:
                yield response.follow(url, callback=self.parseContent, headers=self.headers,
                                      meta={'usedSelenium': True})


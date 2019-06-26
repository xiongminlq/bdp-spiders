# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from news.items import NewsItem
from news.items import CommnetItem
import datetime

class QqspiderSpider(scrapy.Spider):
    name = 'qq'
    allowed_domains = ['qq.com']
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

    # 动态渲染网页初始url
    def start_requests(self):
        start_url = 'http://roll.news.qq.com/#'
        yield scrapy.Request(url=start_url, headers=self.headers, meta={'usedSelenium': True})

    def close(spider, reason):
        spider.driver.close()

    def parseComment(self, response):
        # 解析评论
        comitems = CommnetItem()
        list = response.xpath('//div[@id="J_ShortComment"]')
        user = ''
        commnet = ''
        like = ''
        for index in range(len(list)):
            user = list.xpath('./div/div[2]/p/span[1]/text()').extract_first()
            commnet = list.xpath('./div/div[2]/div[1]/text()').extract_first()
            like =  list.xpath('./div/div[2]/div[3]/span[1]/i/text()').extract_first()
        comitems['user'] = user
        comitems['commnet'] = commnet
        comitems['like'] = like
        yield response.meta['item']


    def parseContent(self, response):
        item = NewsItem()
        item['leadingTitle'] = ''
        item['subTitle'] = ''
        item['source'] = '腾讯网'
        start = response.xpath('//div[@class="qq_article"]')
        # 标题
        title = start.xpath('./div[1]/h1/text()').extract_first()
        item['mainTitle'] = '' if title is None else title.replace('\r', '').replace('\n', '').replace('\t', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        list = response.xpath('//div[@class="a_Info"]/span')
        if len(list) > 0:
            datetext = list[-1].xpath('string()').extract_first()
        if len(list) > 1:
            new_source = list[-2].xpath('string()').extract_first()
        if len(list) > 2:
            new_class = list[-3].xpath('string()').extract_first()
        else:
            new_class = ''
        # 新闻类型
        item['newclass'] = '' if new_class is None else new_class.replace('\r', '').replace('\n', '').replace('\t', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        # 新闻来源
        item['pre_source'] = '' if new_source is None else new_source.replace('\r', '').replace('\n', '').replace('\t',
                                                                                                                  ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        # 新闻时间
        date = ''
        if datetext is not None:
            datetext = datetext.replace('\r', '').replace('\n', '').replace('\xa0', ' '). \
                replace('\u3000', ' ').strip()
            try:
                date = datetime.datetime.strptime(datetext.strip(), "%Y-%m-%d %H:%M")
            except:
                print('时间转换失败。')
        item['date'] = date
        #获取新闻内容
        listcontent = response.xpath('//div[@id="Cnt-Main-Article-QQ"]/p[@class="text"]')
        content = ''
        for index in range(len(listcontent)):
            content += listcontent[index].xpath('string()').extract_first()
        item['content'] = '' if content is None else content.replace('\r', '').replace('\n', '').replace('\t', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        # 获取评论
        commentUrl = response.xpath('//*[@id="cmtLink"]/@href').extract_first()
        # item['content'] = commentUrl
        yield response.follow(commentUrl, callback=self.parseComment, headers=self.headers, meta={'usedSelenium': True,'item': item})
        # if commentUrl is not None:
        #     yield response.follow(commentUrl, callback=self.parseComment, headers=self.headers, meta={'usedSelenium': True})
        # yield item

    def parse(self, response):
        # 获取新闻列表
        news = response.xpath('//li')
        #获取新闻的url
        for new in news:
            url = new.xpath('./a/@href').extract_first()
            if url is not None:
                yield response.follow(url, callback = self.parseContent, headers=self.headers,
                                      meta={'usedSelenium': True})


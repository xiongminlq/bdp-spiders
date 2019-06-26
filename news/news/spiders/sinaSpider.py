# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
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
        dcap["phantomjs.page.settings.resourceTimeout"] = 200000
        dcap["phantomjs.page.settings.loadImages"] = True
        dcap["phantomjs.page.settings.disk-cache"] = True
        dcap["phantomjs.page.settings.userAgent"] = user_agent
        dcap["phantomjs.page.customHeaders.User-Agent"] = user_agent
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ssl-protocol=any'])
        self.driver.set_page_load_timeout(30)
        self.driver.set_window_size(800, 600)

    def start_requests(self):
        start_url = 'https://news.sina.com.cn/china/'
        yield scrapy.Request(url=start_url, headers=self.headers, meta={'usedSelenium': True})

    def close(spider, reason):
        spider.driver.close()

    def parseContent(self, response):
        item = NewsItem()
        item['leadingTitle'] = ''
        item['subTitle'] = ''
        item['source'] = '新浪新闻'
        item['edition'] = ''
        item['anthor'] = ''
        item['url'] = response.url
        title = response.xpath('//div[@class="main-content w1240"]/h1/text()').extract_first()
        item['mainTitle'] = '' if title is None else title.replace('\r', '').replace('\n', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        content = response.xpath('//*[@id="article"]').xpath('string()').extract_first()
        item['content'] = '' if content is None else content.replace('\r', '').replace('\n', ''). \
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        date = ''
        datetext = response.xpath('//div[@class="date-source"]/span/text()').extract_first()
        if datetext is not None:
            datetext = datetext.replace('\r', '').replace('\n', '').replace('\xa0', ' '). \
                replace('\u3000', ' ').strip()
            try:
                date = datetime.datetime.strptime(datetext.strip(), "%Y年%m月%d日 %H:%M")
            except:
                print('时间转换失败')
        item['date'] = date
        yield item

    def parse(self, response):
        newsitem = response.xpath('//div[@class="feed-card-item"]')
        for item in newsitem:
            url = item.xpath('./h2/a/@href').extract_first()
            yield response.follow(url, callback=self.parseContent, meta={'usedSelenium': True})
# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from news.items import CommnetItem
from xlrd import open_workbook
from xlutils.copy import copy


class QqspiderSpider(scrapy.Spider):
    name = 'kq36'
    allowed_domains = ['kq36.com']
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
        url = 'https://www.kq36.com/job_list.asp?Job_ClassII_Id=48&Job_ClassI_Id=2&page='
        for num in range(1, 61):
            page = str(num)
            start_url = url + page
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
            like = list.xpath('./div/div[2]/div[3]/span[1]/i/text()').extract_first()
        comitems['user'] = user
        comitems['commnet'] = commnet
        comitems['like'] = like
        yield response.meta['item']

    def parseContent(self, response):
        i = 0
        r_xls = open_workbook("48.xls")  # 读取excel文件
        row = r_xls.sheets()[0].nrows  # 获取已有的行数
        excel = copy(r_xls)  # 将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(0)  # 获取要操作的sheet
        title = response.xpath('//div[@class="s_company"]/text()').extract_first()
        if title is None:
            title = response.url
        table.write(row, 0, title)
        print(title)
        tds = response.xpath('//div[@class="left"]/div[1]/table[3]/tbody/tr[position()>1]/td')
        for td in tds:
            i = i + 1
            value = ''
            b = td.xpath('./b/text()').extract_first()
            vs = td.xpath('./text()')
            for v in vs:
                value = value + v.extract().strip()
            if b is not None:
                table.write(row, i, value)
        excel.save("48.xls")

    def parse(self, response):
        # 获取新闻列表
        news = response.xpath('//div[@class="li_company"]')
        # 获取新闻的url
        for new in news:
            url = 'https://www.kq36.com' + new.xpath('./a/@href').extract_first()
            print(url)
            title = new.xpath('./a/text()').extract_first()
            if url is not None:
                yield response.follow(url, callback=self.parseContent, headers=self.headers,
                                      meta={'usedSelenium': True})

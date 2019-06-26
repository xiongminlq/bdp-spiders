# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re


class souhuSpider(scrapy.Spider):
    name = 'souhu'
    allowed_domains = ['sohu.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 5
    }
    headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    start_urls = ['http://www.sohu.com/c/8/1460', 'http://police.news.sohu.com/', 'http://learning.sohu.com/']

    def parseContent(self, response):
        item = NewsItem()
        item['leadingTitle'] = ''
        item['subTitle'] = ''
        item['source'] = '搜狐新闻'
        item['edition'] = ''
        item['anthor'] = ''
        item['url'] = response.url
        title = response.xpath('//div[@class="text-title"]/h1/text()').extract_first()
        item['mainTitle'] = '' if title is None else title.replace('\r', '').replace('\n', '').\
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        datetext = response.xpath('//div[@class="article-info"]/span/text()').extract_first()
        date = ''
        if datetext is not None:
            datetext = datetext.replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
            try:
                date = datetime.datetime.strptime(datetext.strip(), "%Y-%m-%d %H:%M")
            except:
                print('时间转换失败')
        item['date'] = date
        content = response.xpath('//*[@id="mp-editor"]').xpath('string()').extract_first()
        item['content'] = '' if content is None else content.replace('\r', '').replace('\n', '').replace('\xa0', ' ').\
            replace('\u3000', ' ').strip()
        yield item

    def parse(self, response):
        newsitem = response.xpath('//div[@data-role="news-item"]')
        for item in newsitem:
            url = item.xpath('./h4/a/@href').extract_first()
            if url is not None:
                url = 'http:' + url
                yield response.follow(url, callback=self.parseContent)
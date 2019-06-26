# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import datetime


class RmwSpider(scrapy.Spider):
    name = 'rmw'
    allowed_domains = ['people.com.cn']
    start_urls = [
        'http://finance.people.com.cn/GB/70846/index.html', 'http://society.people.com.cn/GB/136657/index.html',
        'http://legal.people.com.cn/GB/188502/index.html', 'http://edu.people.com.cn/GB/1053/index.html',
        'http://culture.people.com.cn/GB/172318/index.html', 'http://scitech.people.com.cn/GB/1057/index.html']
    headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }

    def parseContent(self, response):
        item = NewsItem()
        item['leadingTitle'] = ''
        item['mainTitle'] = response.meta['title'].replace('\r', '').replace('\n', '').replace('\xa0', ' ').\
            replace('\u3000', ' ').strip()
        item['subTitle'] = ''
        item['source'] = '人民网'
        date = ''
        datetext = response.xpath('//div[@class="box01"]/div[1]/text()').extract_first()
        if datetext is not None:
            datetext = datetext.replace('\r', '').replace('\n', '').replace('\xa0', ' ').replace('\u3000', ' ').strip()
            index = datetext.find('来源')
            if index > -1:
                datetext = datetext[:index]
                try:
                    date = datetime.datetime.strptime(datetext.strip(), "%Y年%m月%d日%H:%M")
                except:
                    pass
        item['date'] = date
        item['edition'] = ''
        item['anthor'] = ''
        content = ''
        pages = response.xpath('//div[@class="box_con"]/p')
        for p in pages:
            c = p.xpath('./text()').extract_first()
            if c is not None:
                content += c
        item['content'] = '' if content is None else content.replace('\r', '').replace('\n', '').\
            replace('\xa0', ' ').replace('\u3000', ' ').strip()
        item['url'] = response.url
        yield item

    def parse(self, response):
        list = response.xpath('//div[@class="ej_list_box clear"]/ul')
        index = response.url.find('GB')
        base_url = response.url[:index - 1]
        if len(list) > 0:
            for ul in list:
                news = ul.xpath('./li')
                for new in news:
                    title = new.xpath('./a/text()').extract_first()
                    url = base_url + new.xpath('./a/@href').extract_first()
                    yield response.follow(url, callback=self.parseContent, meta={'title': title})
        else:
            list = response.xpath('//div[@class="ej_left"]/ul')
            for ul in list:
                news = ul.xpath('./li')
                for new in news:
                    title = new.xpath('./a/text()').extract_first()
                    url = base_url + new.xpath('./a/@href').extract_first()
                    yield response.follow(url, callback=self.parseContent, meta={'title': title})


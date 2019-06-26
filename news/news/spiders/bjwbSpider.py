# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import datetime


class BjwbSpider(scrapy.Spider):
    name = 'bjwb'
    allowed_domains = ['bjwb.bjd.com.cn']
    # 2017-01/01
    start_urls = []

    def __init__(self):
        url_template = 'http://bjwb.bjd.com.cn/html/{0}/node_113.htm'
        # startDate = datetime.datetime(2018, 12, 23)
        self.endDate = datetime.datetime.now()
        # while startDate <= endDate:
        #     self.start_urls.append(url_template.format(startDate.strftime('%Y-%m/%d')))
        #     startDate += datetime.timedelta(days=1)
        self.start_urls.append(url_template.format(self.endDate.strftime('%Y-%m/%d')))

    def parseContent(self, response):
        article = response.xpath('//div[@class="article"]')
        if article is not None:
            item = NewsItem()
            leadingTitle = article.xpath('./h2[1]/text()').extract_first()
            mainTitle = article.xpath('./h1/text()').extract_first()
            subTitle = article.xpath('./h2[2]/text()').extract_first()
            source = article.xpath('./div[@class="info"]/span[1]/text()').extract_first()
            date = article.xpath('./div[@class="info"]/span[2]/text()').extract_first()
            edition = response.meta['edition']
            edition = edition if edition else article.xpath('./div[@class="info"]/span[4]/text()').extract_first()
            anthor = article.xpath('./div[@class="info"]/span[5]/text()').extract_first()
            item['leadingTitle'] = leadingTitle.replace('\r', '').replace('\n', '').replace('\t', '') \
                .replace('\xa0', ' ').replace('\u3000', ' ').strip()
            item['mainTitle'] = mainTitle.replace('\r', '').replace('\n', '').replace('\t', '') \
                .replace('\xa0', ' ').replace('\u3000', ' ').strip()
            item['subTitle'] = subTitle.replace('\r', '').replace('\n', '').replace('\t', '') \
                .replace('\xa0', ' ').replace('\u3000', ' ').strip()
            item['source'] = source.replace("来源：", "").replace('\r', '').replace('\n', '').replace('\t', '') \
                .replace('\xa0', ' ').replace('\u3000', ' ').strip()
            try:
                item['date'] = self.endDate
            except:
                pass
            item['edition'] = edition.replace("版次：", "").replace('\r', '').replace('\n', '') \
                .replace('\xa0', ' ').replace('\u3000', ' ').strip()
            item['anthor'] = anthor.replace("作者：", "").replace('\r', '').replace('\n', '') \
                .replace('\xa0', ' ').replace('\u3000', ' ').strip()
            text = article.xpath('./div[@class="text"]/p')
            content = ''
            for p in text:
                sub = p.xpath('./text()').extract_first()
                if sub is not None:
                    content += str(sub).replace('\xa0', ' ').replace('\u3000', ' ')
            item['content'] = content
            item['url'] = response.url
            yield item

    def parse(self, response):
        if 'node' in response.url:
            url = response.url[:response.url.rindex('/')+1]
            # 获取新闻正文url
            area_selects = response.xpath('//div[@class="main-list"]/ul/li')
            if area_selects is not None:
                for area_select in area_selects:
                    contenthtm = area_select.xpath('./h2/a/@href').extract_first()
                    if contenthtm is not None:
                        contenthtm = url + contenthtm
                        edition = response.xpath('//div[@class="hd clearfix"]/a[2]').xpath('string()').extract_first()
                        yield scrapy.Request(response.urljoin(contenthtm), callback=self.parseContent, meta={'edition': edition})
            # 获取下一版
            nextUrl = response.xpath('//div[@class="tonextblock"]/a/@href').extract_first()
            if nextUrl is not None:
                nextUrl = url + nextUrl
                yield scrapy.Request(response.urljoin(nextUrl))



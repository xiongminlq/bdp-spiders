# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.htmlnewclass = scrapy.Field()


import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    leadingTitle = scrapy.Field()
    mainTitle = scrapy.Field()
    subTitle = scrapy.Field()
    source = scrapy.Field()
    pre_source = scrapy.Field()
    newclass = scrapy.Field()
    date = scrapy.Field()
    edition = scrapy.Field()
    anthor = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    titleBlod = scrapy.Field()
    description = scrapy.Field()
    tags = scrapy.Field()


class CommnetItem(scrapy.Item):
    user = scrapy.Field()
    commnet = scrapy.Field()
    like = scrapy.Field()


class UserItem(scrapy.Item):
    id = scrapy.Field()  # 用户ID
    nick_name = scrapy.Field()  # 昵称
    gender = scrapy.Field()  # 性别
    province = scrapy.Field()  # 所在省
    city = scrapy.Field()  # 所在城市
    brief_introduction = scrapy.Field()  # 简介
    birthday = scrapy.Field()  # 生日
    crawl_time = scrapy.Field()

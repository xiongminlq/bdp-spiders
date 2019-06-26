# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    name = scrapy.Field()
    corporation = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    address = scrapy.Field()
    registered_capital = scrapy.Field()  # 注册资本
    contributed_capital = scrapy.Field()  # 实缴资本
    status = scrapy.Field()  # 经营状态
    establishment = scrapy.Field()  # 成立日期
    social_code = scrapy.Field()  # 统一社会信用代码
    taxpayer_num = scrapy.Field()  # 纳税人识别号
    registrate_num = scrapy.Field()  # 注册号
    organization_code = scrapy.Field()  # 组织机构代码
    company_type = scrapy.Field()  # 公司类型
    industry_involed = scrapy.Field()  # 所属行业
    approval_date = scrapy.Field()  # 核准日期
    registration_authority = scrapy.Field()  # 登记机关
    area = scrapy.Field()  # 所属地区
    english_name = scrapy.Field()  # 英文名
    used_name = scrapy.Field()  # 曾用名
    insured_num = scrapy.Field()  # 参保人数
    staff_size = scrapy.Field()  # 人员规模
    operate_period = scrapy.Field()  # 营业期限
    business_scope = scrapy.Field()  # 经营范围
    risk = scrapy.Field() #经营异常
# -*- coding: utf-8 -*-
import scrapy
import xlrd
from urllib import parse
from company.items import CompanyItem


class QichachaSpider(scrapy.Spider):
    name = 'qichacha'
    allowed_domains = ['qichacha.com']
    start_urls = []
    start_template_url = 'https://www.qichacha.com/search?key={0}'
    template_url = 'https://www.qichacha.com'
    headers = {
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cookie': 'acw_tc=670f631915460687870798753e301cb9604f5f5382ff66ddd870aaebae; UM_distinctid=167f8e183ac16e-0e154f1fd1eade-323b5b03-1fa400-167f8e183ad93a; zg_did=%7B%22did%22%3A%20%22167f8e18499ec6-075fb17a89cc2f-323b5b03-1fa400-167f8e1849a90c%22%7D; _uab_collina=154606878878525956693654; saveFpTip=true; QCCSESSID=qpjdp3811omp27p3tebrhtuh07; hasShow=1; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1546392305,1546409599,1546412583,1546413680; CNZZDATA1254842228=169452578-1546066864-%7C1546414012; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201546409598680%2C%22updated%22%3A%201546415101928%2C%22info%22%3A%201546068788384%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%221b2f760a9efeb79434b0f0051be870e9%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1546415102',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    def __init__(self):
        book = xlrd.open_workbook('企业数据.xlsx')
        sheet = book.sheet_by_index(0)
        for i in range(1, sheet.nrows):
            value = sheet.cell(i, 2).value.strip()
            if value != '':
                self.start_urls.append(self.start_template_url.format(value))
        # self.start_urls.append(self.start_template_url.format('中铁十六局集团有限公司'))
        # self.start_urls.append(self.start_template_url.format('北京驰德门窗有限公司'))
        # self.start_urls.append(self.start_template_url.format('北京上弦月涮肉坊东坝店'))
        # self.start_urls.append(self.start_template_url.format('北京上弦月涮肉坊东坝店'))
        # self.start_urls.append(self.start_template_url.format('镇江市京口红黄蓝舞厅'))

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.headers)

    def parseDetail(self, response):
        item = {}
        name = response.meta['name']
        item['name'] = name
        item['corporation'] = response.xpath('//div[@class="boss-td"]/div[1]/div[2]/a').xpath('string()').extract_first()
        phone = response.xpath('//div[@class="content"]/div[3]/span[1]/span[2]/span/text()').extract_first()
        item['phone'] = phone.strip().replace('\n', '') if phone else '暂无电话信息'
        website = response.xpath('//div[@class="content"]/div[2]/span[3]/a/@href').extract_first()
        item['website'] = website.strip().replace('\n', '') if website else '暂无网站信息'
        email = response.xpath('//div[@class="content"]/div[3]/span[1]/span[2]/a/text()').extract_first()
        if email:
            item['email'] = email
        else:
            email2 = response.xpath('//div[@class="content"]/div[3]/span[1]/span[2]/text()').extract_first()
            item['email'] = email2.strip().replace('\n', '')
        address = response.xpath('//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[10]/td[2]/text()').extract_first()
        item['address'] = address.strip().replace('\n', '') if address else '暂无地址信息'
        registered_capital = response.xpath('//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[1]/td[2]/text()').extract_first()
        item['registered_capital'] = registered_capital.replace('\n', '').strip() if registered_capital else '暂无注册资本'
        contributed_capital = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[1]/td[4]/text()').extract_first()
        if contributed_capital:
            item['contributed_capital'] = contributed_capital.replace('\n', '').strip()
        else:
            item['contributed_capital'] = '暂无实缴资本'
        status = response.xpath('//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[2]/td[2]/text()').extract_first()
        if status:
            item['status'] = status.replace('\n', '').strip()
        else:
            item['status'] = '暂无经营状态信息'
        establishment = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[2]/td[4]/text()').extract_first()
        if establishment:
            item['establishment'] = establishment.replace('\n', '').strip()
        else:
            item['establishment'] = '暂无成立日期信息'
        social_code = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[3]/td[2]/text()').extract_first()
        if social_code:
            item['social_code'] = social_code.replace('\n', '').strip()
        else:
            item['social_code'] = '暂无统一社会信息代码信息'
        taxpayer_num = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[3]/td[4]/text()').extract_first()
        if taxpayer_num:
            item['taxpayer_num'] = taxpayer_num.replace('\n', '').strip()
        else:
            item['taxpayer_num'] = '暂无纳税人识别号信息'
        registrate_num = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[4]/td[2]/text()').extract_first()
        if registrate_num:
            item['registrate_num'] = registrate_num.replace('\n', '').strip()
        else:
            item['registrate_num'] = '暂无注册号信息'
        organization_code = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[4]/td[4]/text()').extract_first()
        if organization_code:
            item['organization_code'] = organization_code.replace('\n', '').strip()
        else:
            item['organization_code'] = '暂无组织机构代码信息'
        company_type = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[5]/td[2]/text()').extract_first()
        if company_type:
            item['company_type'] = company_type.replace('\n', '').strip()
        else:
            item['company_type'] = '暂无公司类型信息'
        industry_involed = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[5]/td[4]/text()').extract_first()
        if industry_involed:
            item['industry_involed'] = industry_involed.replace('\n', '').strip()
        else:
            item['industry_involed'] = '暂无所属行业信息'
        approval_date = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[6]/td[2]/text()').extract_first()
        if approval_date:
            item['approval_date'] = approval_date.replace('\n', '').strip()
        else:
            item['approval_date'] = '暂无核准日期信息'
        registration_authority = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[6]/td[4]/text()').extract_first()
        if registration_authority:
            item['registration_authority'] = registration_authority.replace('\n', '').strip()
        else:
            item['registration_authority'] = '暂无登记机关信息'
        area = response.xpath('//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[7]/td[2]/text()').extract_first()
        if area:
            item['area'] = area.replace('\n', '').strip()
        else:
            item['area'] = '暂无所属地区信息'
        english_name = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[7]/td[4]/text()').extract_first()
        if english_name:
            item['english_name'] = english_name.replace('\n', '').strip()
        else:
            item['english_name'] = '暂无英文名信息'
        used = response.xpath('//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[8]/td[2]')
        used_name = used.xpath('string(.)').extract_first()
        if used_name:
            item['used_name'] = used_name.replace('\n', '').strip().replace('\xa0', '')
        else:
            item['used_name'] = '暂无曾用名'
        insured_num = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[8]/td[4]/text()').extract_first()
        if insured_num:
            item['insured_num'] = insured_num.replace('\n', '').strip()
        else:
            item['insured_num'] = '暂无参保人数信息'
        staff_size = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[9]/td[2]/text()').extract_first()
        if staff_size:
            item['staff_size'] = staff_size.replace('\n', '').strip()
        else:
            item['staff_size'] = '暂无人员规模信息'
        operate_period = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[9]/td[4]/text()').extract_first()
        if operate_period:
            item['operate_period'] = operate_period.replace('\n', '').strip()
        else:
            item['operate_period'] = '暂无营业期限信息'
        business_scope = response.xpath(
            '//section[@id="Cominfo"]/table[@class="ntable"][2]/tr[11]/td[2]/text()').extract_first()
        if business_scope:
            item['business_scope'] = business_scope.replace('\n', '').strip()
        else:
            item['business_scope'] = '暂无经营范围信息'
        id = response.url[response.url.find('firm_')+5:response.url.find('.html')]
        url = self.template_url + '/company_getinfos?unique=%s&companyname=%s&tab=fengxian' %(id, name)
        # print('url', url)
        yield scrapy.Request(response.urljoin(url) + '#fengxian', headers=self.headers, callback=self.parseRisk,
                             dont_filter=True,meta=item)

    def parseRisk(self, response):
        risk = []
        for i in response.xpath('/html/body/section'):
            if i.xpath('./div[@class="tcaption"]'):
                caption = i.xpath('./div[@class="tcaption"]/h3').xpath('string()').extract_first()
                caption = caption if caption else i.xpath('./div[@class="tcaption"]/span').xpath('string()').extract_first()
                id = i.xpath('./@id').extract_first()
                if id is None and '行政处罚' in caption:
                    id = 'creditlist'
                id = id.lower() if id else id
                datas = []
                for j in i.xpath('./div[@class="clearfix"]'):
                    rows = j.xpath('./section/div/div/div')
                    data = {}
                    for row in rows:
                        key = row.xpath('./small/text()').extract_first()
                        key = key.replace('\r', '').replace('\n', '').strip() if key else ''
                        value = row.xpath('./small/span/text()').extract_first()
                        value = value.replace('\r', '').replace('\n', '').strip() if value else ''
                        data[key] = value
                    datas.append(data)
                for j in i.xpath('./table'):
                    rows = j.xpath('./tr')
                    rows = rows if rows else j.xpath('./tbody/tr')
                    if rows:
                        th = rows.xpath('./th')
                        for row in rows:
                            td = row.xpath('./td')
                            if td:
                                data = {}
                                for k in range(len(th) if len(th) > len(td) else len(td)):
                                    key = th[k].xpath('./text()').extract_first() if k < len(th) else str(k)
                                    key = key if key else str(i)
                                    value = td[k].xpath('string()').extract_first() if k < len(td) else None
                                    value = value.replace('\r', '').replace('\n', '').strip() if value else ''
                                    data[key] = value
                                datas.append(data)
                risk.append({'id': id, 'caption': caption, 'data': datas})
        item = response.meta
        item['risk'] = risk
        yield item

    def parse(self, response):
        searchName = parse.unquote(response.url[response.url.rindex('=')+1:])
        list = response.xpath('//table[@class="m_srchList"]/tbody/tr')
        for i in list:
            name = i.xpath('./td[3]/a').xpath('string()').extract_first()
            if searchName == name:
                url = self.template_url + i.xpath('./td[3]/a/@href').extract_first()
                # url = i.xpath('./td[2]/a/@href').extract_first()
                # yield response.follow(url, callback=self.parseDetail, meta={'name': name},
                #                       dont_filter=True, headers=self.headers)
                yield scrapy.Request(response.urljoin(url) + '#base', headers=self.headers,callback=self.parseDetail,
                                     dont_filter=True,meta={'name': name})

                break

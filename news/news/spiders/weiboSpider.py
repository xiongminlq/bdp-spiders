# -*- coding: utf-8 -*-
import re
from lxml import etree
from selenium.webdriver.common.action_chains import ActionChains
from news.items import UserItem
import time
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WeibospiderSpider(scrapy.Spider):
    name = "weibo"
    base_url = "https://weibo.cn"

    custom_settings = {
        'ITEM_PIPELINES': {'news.pipelines.WeiboPipeline': 321, },
        'DOWNLOAD_DELAY': 10
    }

    def start_requests(self):
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        )
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = user_agent
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver.set_page_load_timeout(30)
        driver.set_window_size(800, 600)
        driver.get('https://weibo.cn')
        assert "微博" in driver.title
        login_link = driver.find_element_by_link_text('登录')
        ActionChains(driver).move_to_element(login_link).click().perform()
        login_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "loginName"))
        )
        login_password = driver.find_element_by_id("loginPassword")
        login_name.send_keys('851946896@qq.com')
        login_password.send_keys('1259407010*wang')
        login_button = driver.find_element_by_id("loginAction")
        login_button.click()
        time.sleep(5)
        cookies = driver.get_cookies()
        print('--------------------------------', cookies[0])
        driver.close()
        start_uids = [
            '2803301701',  # 人民日报
            '1699432410'  # 新华社
        ]
        for uid in start_uids:
            yield scrapy.Request(url="https://weibo.cn/%s/info" % uid, cookies=cookies[0], callback=self.parse_user)

    def parse_user(self, response):
        """ 抓取个人信息 """
        item = UserItem()
        item['crawl_time'] = int(time.time())
        selector = Selector(response)
        text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())
        print('********************', response.url, text1)
        # selector = Selector(response)
        # 获取标签里的所有text()
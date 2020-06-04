# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from ..items import SmartSwitchItem
from selenium import webdriver
from selenium.webdriver.common.actions import input_device
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions


class AlibabaSmartswitchSpider(scrapy.Spider):
    name = 'alibaba_smartswitch'
    allowed_domains = ['alibaba.com']
    start_urls = ['http://alibaba.com/']
    current_url = ''

    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path='C:/ChromeDriverForSelenium/chromedriver')

    def start_requests(self):
        driver = self.driver
        url_main_page = self.start_urls
        driver.implicitly_wait(10)
        driver.get(url_main_page)
        search_textbox = driver.find_element_by_xpath(
            '//div[@id="sticky-searchbar"]//input[@class="ui-searchbar-keyword"]')
        search_textbox.send_keys("smart switch light")
        submit_search = driver.find_element_by_xpath(
            '//div[@class="J-sc-hd-searchbar ui-searchbar ui2-searchbar ui-searchbar-size-middle ui-searchbar-primary ui-searchbar-mod-type ui-searchbar-img-search"]//input[@class="ui-searchbar-submit"]').click()
        window_after = driver.window_handles[0]
        driver.switch_to_window(window_after)
        self.current_url = driver.current_url
        yield scrapy.Request(self.current_url, callback=self.parse)

    def parse(self, response):
        try:
            driver = self.driver
            driver.implicitly_wait(20)
            driver.set_page_load_timeout(20)
            links = driver.find_elements_by_xpath('//div[(@class="list-no-v1-offer-outter J-offer-wrapper increase-pd")]//a[@class ="organic-gallery-title"]')
            urls = [x.get_attribute('href') for x in links]
            for url in urls:
                itemloader = ItemLoader(item=SmartSwitchItem(),selector=url)
                itemloader.add_value('link', url)
                driver.get(url)
                
        except exceptions.NoSuchElementException as identifier:
            print(identifier)
            pass
       
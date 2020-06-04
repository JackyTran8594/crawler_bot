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
from time import sleep
from selenium.webdriver.common.by import By


class AlibabaSmartswitchSpider(scrapy.Spider):
    name = 'alibaba_smartswitch'
    allowed_domains = ['alibaba.com']
    start_urls = 'http://alibaba.com/'
    current_url = ''

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('disable-popup-blocking')
        self.driver = webdriver.Chrome(
            executable_path='C:/ChromeDriverForSelenium/chromedriver', chrome_options=options)
    

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
            links = driver.find_elements_by_xpath(
                '//div[(@class="list-no-v1-offer-outter J-offer-wrapper increase-pd")]//a[@class ="organic-gallery-title"]')
            urls = [x.get_attribute('href') for x in links]
            for url in urls:
                print(url)
                # itemloader = ItemLoader(item=SmartSwitchItem(), selector=url)
                # itemloader.add_value('link', url)
                # driver.get(url)
                # sleep(2)

                # try:
                #     if len(driver.find_elements(By.XPATH, '//div[@class="ma-title-wrap"]//h1[@class="ma-title"]')) > 0:
                #         title = str(driver.find_element_by_xpath(
                #             '//div[@class="ma-title-wrap"]//h1[@class="ma-title"]').text)
                # except exceptions.NoSuchElementException as e:
                #     title = ''
                #     # print(e)
                #     pass

                # if len(driver.find_elements(By.XPATH, '//div[@class="ma-reference-price"]//span[@class="ma-ref-price"]//span')) > 0:
                #     price = str(driver.find_elements(
                #         By.XPATH, '//div[@class="ma-reference-price"]//span[@class="ma-ref-price"]//span')[0].text)
                # else:
                #     price = ''

                # if len(driver.find_elements(By.XPATH, '//div[@class="scc-wrapper detail-module module-productPackagingAndQuickDetail]//div[@class="widget-detail-overview"]')) > 0:
                #     product_detail = str(driver.find_elements(
                #         By.XPATH, '//div[@class="scc-wrapper detail-module module-productPackagingAndQuickDetail]//div[@class="widget-detail-overview"]')[0].text)
                # else:
                #     product_detail = ''

                # if len(driver.find_elements(By.ID, '//div[@class="ife-detail-decorate-table"]//table[@class="hight-light-first-column all magic-4"]')) > 0:
                #     product_info = str(driver.find_elements(
                #         By.ID, '//div[@class="ife-detail-decorate-table"]//table[@class="hight-light-first-column all magic-4"]')[0].text)
                # else:
                #     product_info = ''

                # itemloader.add_value('title', title)
                # itemloader.add_value('price', price)
                # itemloader.add_value('product_detail', product_detail)
                # itemloader.add_value('product_info', product_info)
                # yield itemloader.load_item()

            driver.get(self.current_url)
            sleep(3)

            driver.find_element_by_xpath('//a[@class="seb-pagination__pages-link pages-next"]').click()
            window_after = driver.window_handles[0]
            driver.switch_to_window(window_after)
            next_page_url = driver.current_url
            if next_page_url is not None:
                self.current_url = next_page_url
                yield scrapy.Request(next_page_url, callback=self.parse)

        except exceptions.NoSuchElementException as identifier:
            print(identifier)
            pass

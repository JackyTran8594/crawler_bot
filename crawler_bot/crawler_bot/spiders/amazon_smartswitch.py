# -*- coding: utf-8 -*-
import scrapy
# from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.actions import input_device
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as UI
from selenium.webdriver.support.ui import WebDriverWait

from crawler_bot.items import SmartSwitchItem
from scrapy.loader import ItemLoader
from selenium.common import exceptions


class AmazonSmartswitchSpider(scrapy.Spider):
    name = 'amazon_smartswitch'
    allowed_domains = ['amazon.com']
    start_urls = ['http://amazon.com/']
    # start_urls = ['https://www.amazon.com/s?k=smart+switch+light&ref=nb_sb_noss_2']

    def __init__(self):
       self.driver = webdriver.Chrome(
           'C:/ChromeDriverForSelenium/chromedriver')

    # def start_requests(self, response):
    #     url = start_urls
    #     self.driver.get(response.url)
    #     search_textbox = self.driver.find_element_by_id('twotabsearchtextbox')
    #     search_textbox.send_keys("smart switch light")
    #     div_search = self.driver.find_element_by_id('nav-search')
    #     page_search = div_search.find_element_by_class('nav-input').click()
    #     window_after = self.driver.window_handles[1]
    #     print(window_after)
    #     yield scrapy.Request(self.driver.get(window_after), self.parse)

    def parse(self, response):
        try:
            driver = self.driver
            # driver.set_page_load_timeout(2)
            # driver.set_script_timeout(2)
            driver.implicitly_wait(3)
            driver.get(response.url)
            search_textbox = driver.find_element_by_id('twotabsearchtextbox')
            search_textbox.send_keys("smart switch light")
            div_search = driver.find_element_by_id('nav-search')
            page_search = div_search.find_element_by_class_name(
                'nav-input').click()
            # sleep(2)
            window_after = driver.window_handles[0]
            driver.switch_to.window(window_after)
            links = driver.find_elements_by_xpath(
                '//a[@class="a-link-normal a-text-normal"]')
            # print(links)
            current_window = driver.current_window_handle
            urls = [x.get_attribute('href') for x in links]
            # print(current_window)
            for url in urls:
                itemloader = ItemLoader(item=SmartSwitchItem(), selector=url)
                itemloader.add_value('link', url)
                driver.get(url)

                if driver.find_element_by_id(
                        'priceblock_ourprice').size() != 0:
                    price = driver.find_element_by_id(
                        'priceblock_ourprice').text
                else :
                    price = ''

                try:
                    title = driver.find_element_by_xpath(
                        '//span[@id="productTitle"]').text
                except exceptions.NoSuchCookieException as e:
                    title = ''
                    print(e)


                try:
                   rating = driver.find_element_by_id(
                        'acrCustomerReviewText').text
                except exceptions.NoSuchCookieException as e:
                    rating = ''
                    print(e)


                # try:
                #     price = driver.find_element_by_id(
                #         'priceblock_ourprice').text
                # except exceptions.NoSuchCookieException as e:
                #     price = ''
                #     print(e)


                try:
                   product_info = driver.find_element_by_id(
                                       'feature-bullets').text
                except exceptions.NoSuchCookieException as e:
                    product_info = ''
                    print(e)

                itemloader.add_value('title', title)
                itemloader.add_value('rating', rating)
                itemloader.add_value('price', price)
                # itemloader.add_value('product_detail', product_detail)
                # itemloader.add_value('product_specs', product_specs)
                itemloader.add_value('product_info', product_info)

                itemloader.load_item()
                # driver.close()
                # driver.switch_to_window(current_window)
                sleep(2)

            next_page_url = driver.find_element_by_xpath('//li[@class="a-last"]/a').get_attribute('href')
            if next_page_url is not None:
                # print(next_page_url)
                next_page = response.urljoin(next_page_url)
                yield scrapy.Request(next_page, callback = self.parse)

        except  exceptions.StaleElementReferenceException as e:
            print(e)


        



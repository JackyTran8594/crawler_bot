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
    start_urls = 'http://amazon.com/'
    # start_urls = ['https://www.amazon.com/s?k=smart+switch+light&ref=nb_sb_noss_2']
    current_url =''

    def __init__(self):
        self.driver = webdriver.Chrome(
            'C:/ChromeDriverForSelenium/chromedriver')

    def start_requests(self):
        driver = self.driver
        url = self.start_urls
        driver.implicitly_wait(7)
        # print(url)
        driver.get(url)
        search_textbox = driver.find_element_by_id('twotabsearchtextbox')
        search_textbox.send_keys("smart switch light")
        div_search = driver.find_element_by_id('nav-search')
        page_search = div_search.find_element_by_class_name(
            'nav-input').click()
        window_after = driver.window_handles[0]
        driver.switch_to_window(window_after)
        self.current_url = driver.current_url
        # print(window_after)
        yield scrapy.Request(self.current_url, callback=self.parse)

    def parse(self, response):
        try:
            driver = self.driver
            # driver.set_page_load_timeout(2)
            # driver.set_script_timeout(2)
            driver.implicitly_wait(20)
            driver.set_page_load_timeout(20)
            # driver.get(response.url)
            # search_textbox = driver.find_element_by_id('twotabsearchtextbox')
            # search_textbox.send_keys("smart switch light")
            # div_search = driver.find_element_by_id('nav-search')
            # page_search = div_search.find_element_by_class_name(
            #     'nav-input').click()
            # sleep(2)
            # window_after = driver.window_handles[0]
            # driver.switch_to.window(window_after)
            links = driver.find_elements_by_xpath(
                '//a[@class="a-link-normal a-text-normal"]')
            # print(links)
            # current_window = driver.current_window_handle
            urls = [x.get_attribute('href') for x in links]
            # print(current_window)
            for url in urls:
                # print(url)
                itemloader = ItemLoader(item=SmartSwitchItem(), selector=url)
                itemloader.add_value('link', url)
                # product = itemloader.load_item()
                driver.get(url)
                sleep(2)
                # if url is not None:
                #     driver.get(url)
                #     sleep(2)
                #     url_detail_page = driver.current_url
                #     yield scrapy.Request(url_detail_page, callback=self.parse_detail_page, meta={'product': product})
                try:
                    if len(driver.find_elements(By.XPATH, '//span[@id="productTitle"]')) > 0:
                       title = str(driver.find_element_by_xpath('//span[@id="productTitle"]').text)
                except exceptions.NoSuchElementException as e:
                    title = ''
                    # print(e)
                    pass

                if len(driver.find_elements(By.ID, 'acrCustomerReviewText')) > 0:
                    rating = str(driver.find_elements(By.ID, 'acrCustomerReviewText')[0].text)
                else:
                    rating = ''

                if len(driver.find_elements(By.ID, 'priceblock_ourprice')) > 0:
                    price = str(driver.find_elements(By.ID, 'priceblock_ourprice')[0].text)
                else:
                    price = ''

                if len(driver.find_elements(By.ID, 'feature-bullets')) > 0:
                    product_detail = str(driver.find_elements(By.ID, 'feature-bullets')[0].text)
                else:
                    product_detail = ''

                if len(driver.find_elements(By.ID, 'productDetails_techSpec_section_1')) > 0:
                    product_specs = str(driver.find_elements(By.ID, 'productDetails_techSpec_section_1')[0].text)
                else:
                    product_specs = ''

                if len(driver.find_elements(By.ID, 'feature-bullets')) > 0:
                    product_info = str(driver.find_elements(By.ID, 'feature-bullets')[0].text)
                else:
                    product_info = ''

                itemloader.add_value('title', title)
                itemloader.add_value('rating', rating)
                itemloader.add_value('price', price)
                itemloader.add_value('product_detail', product_detail)
                itemloader.add_value('product_specs', product_specs)
                itemloader.add_value('product_info', product_info)
                yield itemloader.load_item()

            driver.get(self.current_url)
            sleep(3)
                # driver.close()

            next_page_url = driver.find_element_by_xpath(
                '//li[@class="a-last"]/a').get_attribute('href')
            if next_page_url is not None:
                print(next_page_url)
                # next_page = response.urljoin(next_page_url)
                driver.get(next_page_url)
                url_by_page = driver.current_url
                self.current_url = url_by_page
                # print(url_by_page)
                yield scrapy.Request(url_by_page, callback=self.parse)

        except exceptions.StaleElementReferenceException as e:
            print(e)

    def parse_detail_page(self, response):
        driver = self.driver
        driver.implicitly_wait(5)
        driver.set_page_load_timeout(5)
        # driver.
        product = response.meta['product']
        # if len(driver.find_elements(By.ID, '//span[@id="productTitle"]')) > 0:
        #     title = driver.find_elements(
        #         By.XPATH, '//span[@id="productTitle"]')[0].text
        # else:
        #     title = ''

        # try:
        #     title = driver.find_element_by_xpath('//span[@id="productTitle"]').text[0]
        # except exceptions.NoSuchCookieException as e:
        #     title = ''
        #     print(e)

        # if len(driver.find_elements(By.ID, 'acrCustomerReviewText')) > 0:
        #     rating = driver.find_elements(By.ID, 'acrCustomerReviewText')[0].text[0]
        # else:
        #     rating = ''

        # if len(driver.find_elements(By.ID, 'priceblock_ourprice')) > 0:
        #     price = driver.find_elements(By.ID, 'priceblock_ourprice')[0].text[0]
        # else:
        #     price = ''

        # if len(driver.find_elements(By.ID, 'feature-bullets')) > 0:
        #     product_detail = driver.find_elements(By.ID, 'feature-bullets')[0].text[0]
        # else:
        #     product_detail = ''

        # if len(driver.find_elements(By.ID, 'productDetails_techSpec_section_1')) > 0:
        #     product_specs = driver.find_elements(By.ID, 'productDetails_techSpec_section_1')[0].text[0]
        # else:
        #     product_specs = ''

        # if len(driver.find_elements(By.ID, 'feature-bullets')) > 0:
        #     product_info = driver.find_elements(By.ID, 'feature-bullets')[0].text[0]
        # else:
        #     product_info = ''

        # product_detail = driver.find_element_by_id('feature-bullets').text
        # product_specs = driver.find_element_by_id('productDetails_techSpec_section_1').text

        detail_loader = ItemLoader(item=product, response = response)
        # detail_loader.add_value('title', title)
        # detail_loader.add_value('rating', rating)
        # detail_loader.add_value('price', price)
        # detail_loader.add_value('product_detail', product_detail)
        # detail_loader.add_value('product_specs', product_specs)
        # detail_loader.add_value('product_info', product_info)
        yield detail_loader.load_item()


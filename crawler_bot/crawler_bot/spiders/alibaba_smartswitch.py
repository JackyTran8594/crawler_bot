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
from selenium.webdriver.support import expected_conditions as EC


class AlibabaSmartswitchSpider(scrapy.Spider):
    name = 'alibaba_smartswitch'
    allowed_domains = ['alibaba.com']
    start_urls = 'http://alibaba.com/'
    current_url = ''
    urls_page =[]

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-popup-blocking')
        self.driver = webdriver.Chrome(
            executable_path='C:/ChromeDriverForSelenium/chromedriver', chrome_options=options)

    def start_requests(self):
        driver = self.driver
        url_main_page = self.start_urls
        driver.implicitly_wait(30)
        driver.set_page_load_timeout(30)
        driver.get(url_main_page)
        sleep(2)
        driver.find_element_by_xpath('//a[(@class="double-close")]').click()
        search_textbox = driver.find_element_by_xpath(
            '//div[@class="J-sc-hd-searchbar ui-searchbar ui2-searchbar ui-searchbar-size-middle ui-searchbar-primary ui-searchbar-mod-type ui-searchbar-img-search"]//div[@class="ui-searchbar-main"]//input[@class="ui-searchbar-keyword"]')
        # print(search_textbox)
        search_textbox.send_keys("smart switch light" + Keys.ENTER)
        sleep(5)
        end_page = driver.find_element_by_xpath("//div[@class='seb-pagination']//a[contains(text(),'" + 'End'  + "')]").get_attribute('href')
        main_url = end_page[:-3]
        number_of_page = end_page[-3:]
        for i in range(1, int(number_of_page) + 1):
            url = main_url + str(i)
            self.urls_page.append(url)

        window_after = driver.window_handles[0]
        driver.switch_to_window(window_after)
        self.current_url = driver.current_url      
        yield scrapy.Request(self.current_url, callback=self.parse)
            

    def parse(self, response):
        try:
            driver=self.driver
            driver.implicitly_wait(30)
            driver.set_page_load_timeout(30)
           
            for url_page in self.urls_page: 
                if url_page[-1] != 1:
                    driver.get(url_page)
                    links=driver.find_elements_by_xpath(
                                    # "//div[contains(@class,'organic-list-offer-center')]//a[contains(@class,'organic-gallery-title')]"
                                    "//a[contains(@class,'organic-gallery-title')]"
                                    )
                    print(links)
                    urls=[x.get_attribute('href') for x in links]
                    for url in urls:
                        orders = []
                        prices = []
                        itemloader = ItemLoader(item=SmartSwitchItem(), selector=url)
                        itemloader.add_value('link', url)
                        driver.get(url)
                        sleep(2)

                        try:
                            if len(driver.find_elements(By.XPATH, '//div[@class="ma-title-wrap"]//h1[@class="ma-title"]')) > 0:
                                title = str(driver.find_element_by_xpath(
                                    '//div[@class="ma-title-wrap"]//h1[@class="ma-title"]').text)
                        except exceptions.NoSuchElementException as e:
                            title = ''
                            # print(e)
                            pass

                        if len(driver.find_elements(By.XPATH, '//div[@class="ma-reference-price"]//span[@class="ma-ref-price"]//span')) > 0:
                            price = str(driver.find_elements(
                                By.XPATH, '//div[@class="ma-reference-price"]//span[@class="ma-ref-price"]//span')[0].text)
                        else:
                            price = ''

                        if len(driver.find_elements(By.XPATH, '//div[@class="scc-wrapper detail-module module-productPackagingAndQuickDetail"]//div[@class="widget-detail-overview"]')) > 0:
                            product_detail = str(driver.find_elements(
                                By.XPATH, '//div[@class="scc-wrapper detail-module module-productPackagingAndQuickDetail"]//div[@class="widget-detail-overview"]')[0].text)
                        else:
                            product_detail = ''

                        # if len(driver.find_elements(By.ID, '//div[@class="ife-detail-decorate-table"]//table[@class="hight-light-first-column all magic-4"]')) > 0:
                        #     product_info = str(driver.find_elements(
                        #         By.ID, '//div[@class="ife-detail-decorate-table"]//table[@class="hight-light-first-column all magic-4"]')[0].text)
                        # else:
                        #     product_info = ''

                        if len(driver.find_elements(By.XPATH, '//div[@class="ma-main"]//div[@class="ma-quantity-range"]')) > 0:
                            orders = driver.find_elements(By.XPATH, '//div[@class="ma-main"]//div[@class="ma-quantity-range"]')
                            min_order = str(orders[0].text)
                            medium_order = orders[1].text
                            large_order = orders[2].text
                        
                        if len(driver.find_elements(By.XPATH, '//div[@class="ma-main"]//div[@class="ma-spec-price ma-price-promotion"]')) > 0:
                            prices = driver.find_elements(By.XPATH, '//div[@class="ma-main"]//div[@class="ma-spec-price ma-price-promotion"]')
                            min_order_price = prices[0].text
                            medium_order_price = prices[1].text
                            large_order_price = prices[2].text


                        itemloader.add_value('title', title)
                        itemloader.add_value('price', price)
                        itemloader.add_value('product_detail', product_detail)
                        itemloader.add_value('min_order', min_order)
                        itemloader.add_value('medium_order', medium_order)
                        itemloader.add_value('large_order', large_order)
                        itemloader.add_value('min_order_price', min_order_price)
                        itemloader.add_value('medium_order_price', medium_order_price)
                        itemloader.add_value('large_order_price', large_order_price)


                        # itemloader.add_value('product_info', product_info)
                        yield itemloader.load_item()

 


        except exceptions.NoSuchElementException as identifier:
            print(identifier)
            pass

# -*- coding: utf-8 -*-
import scrapy
# from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.actions import input_device
from selenium.webdriver.common.keys import Keys


class AmazonSmartswitchSpider(scrapy.Spider):
    name = 'amazon_smartswitch'
    allowed_domains = ['amazon.com']
    start_urls = ['http://amazon.com/']

    
    def __init__(self):
       self.driver = webdriver.Chrome('C:/ChromeDriverForSelenium/chromedriver')

    # def start_requests(self, response):
    #     url = start_urls
    #     self.driver.get(response.url)
    #     yield scrapy.Request(url, self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        search_textbox = self.driver.find_element_by_id('twotabsearchtextbox')
        search_textbox.send_keys("smart switch light")
        div_search = self.driver.find_element_by_id('nav-search')
        page_search = div_search.find_element_by_class('nav-input').click()
        

        pass

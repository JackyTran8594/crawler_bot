# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from ..items import SmartSwitchItem;


class AlibabaSmartswitchSpider(scrapy.Spider):
    name = 'alibaba_smartswitch'
    allowed_domains = ['alibaba.com']
    start_urls = ['http://alibaba.com/']
    produts = SmartSwitchItem()

    def parse(self, response):
        links = response.css("h2.title a::attr(href)").extract()
        for link in links:
            loader = ItemLoader(item=SmartSwitchItem(), selector=link)
            loader.add_value('link', link)
            product = loader.load_item()
            if link is not None:
                req_detail = scrapy.Request(
                link, callback=self.parse_detail_page, meta={'product': product})
                yield req_detail


            next_page_url = response.xpath('//a[contains(@class,"next i-next")]//@href').extract_first()
            
            if next_page_url is not None:
                print(next_page_url)
                next_page = response.urljoin(next_page_url)
                yield scrapy.Request(next_page, callback=self.parse)

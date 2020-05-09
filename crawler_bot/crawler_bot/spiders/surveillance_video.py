# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import CrawlerBotItem


class SurveillanceVideoSpider(scrapy.Spider):
    produts = CrawlerBotItem()
    name = 'surveillance_video'
    allowed_domains = ['surveillance-video.com']
    start_urls = ['https://www.surveillance-video.com/cameras/']
    #url_base = 'https://www.surveillance-video.com/bullet-cameras/shopby/day-night-+audio/m-jpeg-+h-265--+h-264--/network-ip/?dir=asc&limit=50&mode=grid&order=price&'

    def parse(self, response):

            for sel in response.css("li.item odd"):
                link = sel.css("h2.product-name > a::attr(href)").extract_first()
                if link is not None:
                    req_detail = response.follow(link, callback=self.parse_detail_page)
                    yield req_detail
            
            next_page_url = response.css("div.tool-bar-bottom-mobile div.pages a::attr(href)").getall()
    
            if next_page_url is not None:
                next_page_url = response.urljoin(next_page_url[4])
                yield scrapy.Request(next_page_url, callback=self.parse)

    
    def parse_detail_page(self, response):
        title = response.css("div.product-name > h1").extract()
        sku = response.css("div.product_model_desktop > span > h3 > span").extract_first()
        model = response.css("div.product_model_desktop > span > h3 + h3 > span").extract()
        price = response.css("div.prince-info  span[class=price]").extract()
        product_detail = response.css("div#description_tabbed .std").extract()
        product_specs = response.css("div#additional_tabbed #product-attribute-specs-table").extract()

        produts['title'] = title
        produts['sku'] = sku
        produts['model'] = model
        produts['price'] = price
        produts['product_detail'] = product_detail
        produts['product_specs'] = product_specs

        yield produts




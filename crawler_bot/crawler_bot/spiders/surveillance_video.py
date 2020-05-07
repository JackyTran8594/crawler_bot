# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import CrawlerBotItem


class SurveillanceVideoSpider(scrapy.Spider):
    produts = CrawlerBotItem()
    name = 'surveillance_video'
    allowed_domains = ['surveillance-video.com.com']
    start_urls = ['https://www.surveillance-video.com/']
    url_base = 'https://www.surveillance-video.com/bullet-cameras/shopby/day-night-+audio/m-jpeg-+h-265--+h-264--/network-ip/?dir=asc&limit=50&mode=grid&order=price&'
    #url_2 = 'https://www.surveillance-video.com
    # /bullet-cameras/shopby/day-night-+audio/m-jpeg-+h-265--+h-264--/
    # network-ip/?dir=asc&limit=50&mode=grid&order=price&p=2'
    pages = range(1,17)
    urls = []
    link_detail_product = []




    def parse(self, response):
        #for url in urls:
           # print(url)
           # req = scrapy.Request(url, callback=self.parse_links)
           # yield req
         for sel in response.css("div.details-area"):
            link = sel.css("h2.product-name > a::attr(href)").extract_first()
            if link is not None:
               req_detail = scrapy.Request(link, callback=self.parse_detail_page)
               yield req_detail
        
         next_page_url = response.css("div.pages a[class=next i-next]::attr(href)")
         if next_page_url is not None:
             yield scrapy.Request(response.urljoin(next_page_url))

    #def parse_links(self, response):
      #  for sel in response.css("div.details-area"):
       #     link = sel.css("h2.product-name > a::attr(href)").extract_first()
        #    link_detail_product.append(link)
            #if link is not None:
               #req_detail = scrapy.Request(link, callback=self.parse_detail_page)
         #   yield link_detail_product


    
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




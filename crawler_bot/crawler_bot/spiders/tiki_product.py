# -*- coding: utf-8 -*-
import scrapy


class TikiProductSpider(scrapy.Spider):
    name = 'tiki_product'
    allowed_domains = ['tiki.com']
    start_urls = ['http://tiki.com/']

    def parse(self, response):
            links = response.css("div.EdgeBanner__Wrapper-sc-1ubmrcp-0 dCQjxq a::attr(href)").extract()
            for link in links:                
                loader = ItemLoader(item=CrawlerBotItem(), selector= link)
                loader.add_value('link', link)
                product = loader.load_item()
                if link is not None:
                    req_detail = scrapy.Request(link, callback=self.parse_detail_page, meta ={'product': product})
                    yield req_detail
      

            next_page_url = response.xpath('//a[contains(@class,"next i-next")]//@href').extract_first()
    
            if next_page_url is not None:
                print(next_page_url)
                next_page = response.urljoin(next_page_url)
                yield scrapy.Request(next_page, callback=self.parse)
        

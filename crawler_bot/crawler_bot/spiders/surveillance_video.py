# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from ..items import CrawlerBotItem


class SurveillanceVideoSpider(scrapy.Spider):
    produts = CrawlerBotItem()
    name = 'surveillance_video'
    allowed_domains = ['surveillance-video.com']
    #start_urls = ['https://www.surveillance-video.com/cameras/']
    # bullet-camera
    start_urls = ['https://www.surveillance-video.com/bullet-cameras/shopby/h-264--/network-ip/?']
    # dome-camera
    #start_urls = ['https://www.surveillance-video.com/dome-cameras/shopby/network-ip/?']
    # ptz-camera
    #start_urls = ['https://www.surveillance-video.com/ptz-cameras/shopby/network-ip/']

    def parse(self, response):
            links = response.css("div.productdescpart a::attr(href)").extract()
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
            

    
    def parse_detail_page(self, response):
       
        product = response.meta['product']
        
        title = response.css('div.product-name  h1::text').get()
        sku_model = response.xpath('//div[contains(@class, "product_model_desktop")]//h3//span/text()').getall()
        sku = sku_model[0]
        model = sku_model[1]
        price = response.xpath('//div[contains(@class, "price-box")]//span//span//span/text()').get()
        product_detail_p = response.css("div#description_tabbed div.std p::text").extract()
        product_detail_li = response.css("div#description_tabbed div.std ul li::text").extract()
        product_detail = response.css("div#description_tabbed div.std").extract()
        product_specs_th = list(dict.fromkeys(response.css("div#additional_tabbed table#product-attribute-specs-table tbody tr th::text").extract()))
        product_specs = response.css("div#additional_tabbed table#product-attribute-specs-table").extract()
        features_common = response.css("div#additional_tabbed table#product-attribute-specs-table tbody tr td::text").getall()
        #tr_lst = response.css("div#additional_tabbed table#product-attribute-specs-table tbody tr").extract()
            

        try:
            # manufacturer_id = label.index('Manufacturer')
            manufacturer = features_common[1]
        except ValueError as e:
            manufacturer = ''

        try:
            #  features_id = label.index('Features')
             features = features_common[2]
        except ValueError as e:
             features = ''

        try:
            #  camera_signal_id = label.index('Camera Signal')
             camera_signal = features_common[3]
        except ValueError as e:
             camera_signal = ''

        # try:
        #     resolution_id = label.index('Resolution')
        #     resolution = features_common[resolution_id]
        # except ValueError as e:
        #     resolution = ''

        # try:
        #     infrared_distance_id = label.index('Infrared Distance')
        #     infrared_distance = features_common[infrared_distance_id]
        # except ValueError as e:
        #     infrared_distance = ''

        # try:
        #     sensor_option_id = label.index('Sensor Option')        
        #     sensor_option = features_common[sensor_option_id]
        # except ValueError as e:
        #     sensor_option = ''

        # try:
        #     lens_type_id = label.index('Lens Type')
        #     lens_type = features_common[lens_type_id]
        # except ValueError as e:
        #     lens_type = ''

        # try:
        #     lens_size_id = label.index('Lens Size')
        #     lens_size = features_common[lens_size_id]
        # except ValueError as e:
        #     lens_size = ''

        # try:  
        #     durability_id = label.index('Durability')
        #     durability = features_common[durability_id]
        # except ValueError as e:
        #     durability = ''


        loader_detail = ItemLoader(item=product, response = response)
        loader_detail.add_value('title', title)
        loader_detail.add_value('sku',sku_model[0])
        loader_detail.add_value('model',sku_model[1])
        loader_detail.add_value('manufacturer', manufacturer)
        loader_detail.add_value('features', features)
        loader_detail.add_value('camera_signal', camera_signal)
        #loader_detail.add_value('resolution', resolution)
        #loader_detail.add_value('sensor_option', sensor_option)
        #loader_detail.add_value('lens_type', lens_type)
        #loader_detail.add_value('lens_size', lens_size)
        #loader_detail.add_value('infrared_distance', infrared_distance)
        #loader_detail.add_value('durability', durability)
        loader_detail.add_value('price', price)
        loader_detail.add_value('product_detail', product_detail)
        loader_detail.add_value('product_specs', product_specs)

        #yield {
        #    'title' : title,
        #    'sku': sku,
        #    'model': model,
        #    'price': price,
        #    'product_detail':product_detail,
        #    'product_specs':product_specs
        #}
        yield loader_detail.load_item()




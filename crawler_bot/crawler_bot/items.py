# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerBotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    sku = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    product_detail = scrapy.Field()
    product_specs = scrapy.Field()
    link = scrapy.Field()
    manufacturer = scrapy.Field()
    features = scrapy.Field()
    camera_signal = scrapy.Field()
    resolution = scrapy.Field()
    sensor_option = scrapy.Field()
    lens_type = scrapy.Field()
    lens_size = scrapy.Field()
    infrared_distance = scrapy.Field()
    durability = scrapy.Field()
    pass

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from crawler_app.myapp.models import Product

class SurveillanceItem(scrapy.Item):
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


class ProductItem(scrapy.Item):
    title = scrapy.Field()
    sku = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    product_detail = scrapy.Field()
    product_specs = scrapy.Field()
    link = scrapy.Field()
    manufacturer = scrapy.Field()
    category = scrapy.Field()
    pass


class CategoryItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    pass


class SmartSwitchItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    sku = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    product_detail = scrapy.Field()
    product_specs = scrapy.Field()
    product_info = scrapy.Field()
    link = scrapy.Field()
    manufacturer = scrapy.Field()
    features = scrapy.Field()
    min_order = scrapy.Field()
    medium_order = scrapy.Field()
    large_order = scrapy.Field()
    min_order_price = scrapy.Field()
    medium_order_price = scrapy.Field()
    large_order_price = scrapy.Field()
    pass


class Product(DjangoItem):
    django_model = Product
from django.db import models
from django.utils import timezone

# Create your models here.


class Product(models.Model):
    product_id = models.CharField(max_length=255)
    title = models.TextField()
    sku = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    price = models.IntegerField()
    product_detail = models.TextField()
    product_specs = models.TextField()
    link = models.TextField()
    manufacturer = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    # datetime for the first save record
    date_save = models.DateTimeField()
    data_update = models.DateTimeField()
    manufacturer = models.TextField()
    made_in = models.TextField()
    ecommercial_id = models.CharField(max_length=255)
    providers_id = models.CharField(max_length=255)
    reviews = models.IntegerField()
    rank = models.IntegerField()
    average_rating = models.FloatField()
    name_of_rank = models.TextField()

    def __str__(self):
        return self.product_id


class Category(models.Model):
    category_id = models.CharField(max_length=255)
    name = models.TextField()
    # datetime for the first save record
    data_save = models.DateTimeField()
    data_update = models.DateTimeField()
    year_member = models.IntegerField()
    provider_type = models.TextField()
    note = models.TextField()
    ecommercial_name = models.TextField()

    def __str__(self):
        return self.category_id


class Provider(models.Model):
    provider_id = models.CharField(max_length=255)
    name = models.TextField()
    year_member = models.IntegerField()
    provider_type = models.TextField()
    # datetime for the first save record
    data_save = models.DateTimeField()
    data_update = models.DateTimeField()
    note = models.TextField()

    def __str__(self):
        return self.provider_id

from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.TextField()
    sku = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    price = models.IntegerField()
    product_detail = models.TextField()
    product_specs = models.TextField()
    link = models.TextField()
    manufacturer = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
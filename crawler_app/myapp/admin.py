from django.contrib import admin
from . import models

# Register your models here.
class CrawlerAppAdmin(admin.ModelAdmin):
    list_display = "something"

admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Provider)
